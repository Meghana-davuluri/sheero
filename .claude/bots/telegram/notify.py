#!/usr/bin/env python3
"""Send a scheduled push notification to your via the Sheero Telegram bot.

Usage: notify.py {morning|midday}
"""
import os
import sys
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

ENV_FILE = Path.home() / ".config" / "sheero" / "telegram.env"

MESSAGES = {
    "morning": (
        "Good morning! Ready to start the day?\n\n"
        "Reply 'good morning' for your full check-in (journal, calendar, weather, tasks), "
        "or just tell me what's on your plate."
    ),
    "midday": (
        "Midday check — how's the day going?\n\n"
        "What have you finished so far, what's still on the plate, "
        "and is anything blocking you?"
    ),
}


def load_env(path: Path) -> None:
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


def send_message(token: str, chat_id: str, text: str) -> None:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=10) as resp:
        if resp.status != 200:
            raise RuntimeError(f"Telegram API error: {resp.status}")


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in MESSAGES:
        sys.exit(f"usage: {sys.argv[0]} {{{'|'.join(MESSAGES)}}}")
    if not ENV_FILE.exists():
        sys.exit(f"ERROR: env file not found at {ENV_FILE}")
    load_env(ENV_FILE)
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    owner = os.environ.get("TELEGRAM_OWNER_ID")
    if not token or not owner:
        sys.exit("ERROR: missing TELEGRAM_BOT_TOKEN or TELEGRAM_OWNER_ID")
    slot = sys.argv[1]
    send_message(token, owner, MESSAGES[slot])
    print(f"Sent {slot} push at {datetime.now():%Y-%m-%d %H:%M}")


if __name__ == "__main__":
    main()
