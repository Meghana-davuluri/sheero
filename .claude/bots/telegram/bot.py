#!/usr/bin/env python3
"""Sheero Telegram bot — routes messages to Claude Code with the brain as CWD."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import sys
import time
from collections import defaultdict, deque
from datetime import date, datetime
from pathlib import Path
from typing import Optional, Tuple

BRAIN_DIR = Path("~/sheero")
INBOX_DIR = BRAIN_DIR / "cortex" / "inbox"
CONFIG_DIR = Path.home() / ".config" / "sheero"
ENV_FILE = CONFIG_DIR / "telegram.env"
SESSIONS_FILE = CONFIG_DIR / "sessions.json"
SPEND_FILE = CONFIG_DIR / "daily_spend.json"


def load_env_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


load_env_file(ENV_FILE)

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OWNER_ID = int(os.environ["TELEGRAM_OWNER_ID"])
DAILY_CAP = float(os.environ.get("DAILY_COST_CAP_USD", "5.00"))
CLAUDE_BIN = os.environ.get("CLAUDE_BIN", "/opt/homebrew/bin/claude")

COST_PER_1M_INPUT = 3.00
COST_PER_1M_OUTPUT = 15.00

RATE_WINDOW_SEC = 60
RATE_MAX = 10
_rate_log: dict[int, deque] = defaultdict(deque)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger("sheero")


def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except Exception:
        log.exception("Failed to parse %s, using default", path)
        return default


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))


def get_session_id(user_id: int) -> str | None:
    return load_json(SESSIONS_FILE, {}).get(str(user_id))


def set_session_id(user_id: int, session_id: str) -> None:
    sessions = load_json(SESSIONS_FILE, {})
    sessions[str(user_id)] = session_id
    save_json(SESSIONS_FILE, sessions)


def clear_session(user_id: int) -> None:
    sessions = load_json(SESSIONS_FILE, {})
    sessions.pop(str(user_id), None)
    save_json(SESSIONS_FILE, sessions)


def get_today_spend() -> float:
    return float(load_json(SPEND_FILE, {}).get(str(date.today()), 0.0))


def add_spend(amount: float) -> None:
    data = load_json(SPEND_FILE, {})
    today = str(date.today())
    data[today] = float(data.get(today, 0.0)) + amount
    cutoff = date.today().toordinal() - 30
    data = {k: v for k, v in data.items() if date.fromisoformat(k).toordinal() >= cutoff}
    save_json(SPEND_FILE, data)


def is_owner(update: Update) -> bool:
    uid = update.effective_user.id if update.effective_user else None
    if uid != OWNER_ID:
        uname = update.effective_user.username if update.effective_user else None
        log.warning("REJECTED message from user_id=%s username=%s", uid, uname)
        return False
    return True


def rate_limit_ok(user_id: int) -> bool:
    now = time.time()
    q = _rate_log[user_id]
    while q and q[0] < now - RATE_WINDOW_SEC:
        q.popleft()
    if len(q) >= RATE_MAX:
        return False
    q.append(now)
    return True


async def call_claude(user_message: str, session_id: str | None) -> tuple[str, str | None, float]:
    cmd = [CLAUDE_BIN, "-p", user_message, "--output-format", "json"]
    if session_id:
        cmd += ["--resume", session_id]
    log.info("claude invoke: resume=%s len=%d", session_id, len(user_message))
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        cwd=str(BRAIN_DIR),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env={**os.environ},
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        err = stderr.decode()[:500]
        log.error("claude exit=%d stderr=%s", proc.returncode, err)
        raise RuntimeError(f"claude exited {proc.returncode}: {err[:200]}")
    try:
        parsed = json.loads(stdout.decode())
    except json.JSONDecodeError:
        log.error("claude non-JSON output: %s", stdout.decode()[:500])
        raise RuntimeError("claude returned non-JSON output")
    reply = (parsed.get("result") or "").strip() or "(empty response)"
    new_session = parsed.get("session_id")
    usage = parsed.get("usage", {}) or {}
    cost = (
        usage.get("input_tokens", 0) * COST_PER_1M_INPUT / 1_000_000
        + usage.get("output_tokens", 0) * COST_PER_1M_OUTPUT / 1_000_000
    )
    return reply, new_session, cost


async def send_long(message, text: str) -> None:
    limit = 4000
    if len(text) <= limit:
        await message.reply_text(text)
        return
    for i in range(0, len(text), limit):
        await message.reply_text(text[i : i + limit])


async def on_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_owner(update):
        return
    user_id = update.effective_user.id
    if not rate_limit_ok(user_id):
        await update.message.reply_text("Rate limit: 10 msgs/min. Slow down.")
        return
    if get_today_spend() >= DAILY_CAP:
        await update.message.reply_text(
            f"Daily cost cap hit (${DAILY_CAP:.2f}). Resumes at midnight."
        )
        return
    msg_text = update.message.text
    if not msg_text:
        return
    await ctx.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )
    try:
        session = get_session_id(user_id)
        reply, new_session, cost = await call_claude(msg_text, session)
        if new_session:
            set_session_id(user_id, new_session)
        add_spend(cost)
        await send_long(update.message, reply)
        log.info("msg done cost=$%.4f today=$%.4f", cost, get_today_spend())
    except Exception as e:
        log.exception("Error in on_text")
        await update.message.reply_text(f"Bot error: {str(e)[:200]}. Check logs.")


async def on_media(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_owner(update):
        return
    msg = update.message
    caption = (msg.caption or "").strip()
    safe = re.sub(r"[^a-zA-Z0-9_-]", "_", caption)[:40]
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    file_obj = None
    ext = "bin"
    if msg.photo:
        file_obj = await msg.photo[-1].get_file()
        ext = "jpg"
    elif msg.document:
        file_obj = await msg.document.get_file()
        ext = Path(msg.document.file_name or "").suffix.lstrip(".") or "bin"

    if not file_obj:
        return
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{ts}_{safe}.{ext}" if safe else f"{ts}.{ext}"
    dest = INBOX_DIR / filename
    await file_obj.download_to_drive(str(dest))
    log.info("Saved inbox file: %s", dest)
    await msg.reply_text(f"Saved to inbox as {filename}. Will process at evening check-in.")


async def on_status(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_owner(update):
        return
    spend = get_today_spend()
    session = get_session_id(update.effective_user.id)
    await update.message.reply_text(
        f"Sheero bot up.\n"
        f"Today's spend: ${spend:.4f} / ${DAILY_CAP:.2f}\n"
        f"Active session: {session or '(none — next msg starts fresh)'}"
    )


async def on_reset(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_owner(update):
        return
    clear_session(update.effective_user.id)
    await update.message.reply_text("Session reset. Next message starts a new conversation.")


def main() -> None:
    log.info("Starting Sheero Telegram bot")
    log.info("Brain dir: %s", BRAIN_DIR)
    log.info("Owner ID: %s", OWNER_ID)
    log.info("Daily cap: $%.2f", DAILY_CAP)
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("status", on_status))
    app.add_handler(CommandHandler("reset", on_reset))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, on_media))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
