# Sheero Telegram Bot

Persistent daemon that routes Telegram messages from your phone to Claude Code with `~/sheero` as the working directory.

## How it works

```
Phone (Telegram) <─> @YourBot <─> bot.py (launchd) <─> claude -p (brain cwd)
```

- Long-polls the Telegram Bot API (no webhook, no public endpoint)
- Whitelisted to your Telegram user ID — all other senders are silently dropped
- Text messages → invoke `claude -p --output-format json --resume <session>` → reply with `result`
- Photos/documents → save to `cortex/inbox/` with a timestamped name
- `/status` shows uptime + today's spend + active session
- `/reset` clears the Claude session (next message starts fresh)

## Secrets (NOT in repo)

Live at `~/.config/sheero/telegram.env` with `chmod 600`:

```
TELEGRAM_BOT_TOKEN=...        # from @BotFather
TELEGRAM_OWNER_ID=...         # your numeric Telegram user ID
CLAUDE_CODE_OAUTH_TOKEN=...   # from `claude setup-token`
DAILY_COST_CAP_USD=5.00
CLAUDE_BIN=~/.local/bin/claude
```

Rotating the bot token: `@BotFather` → `/revoke` → `@YourBot` → paste new token into the env file → `launchctl kickstart -k gui/$(id -u)/com.example.telegram`.

## Start / stop

The launchd plist lives at `~/Library/LaunchAgents/com.example.telegram.plist`. A copy of the source lives here at `com.example.telegram.plist` (update this one, then reinstall).

```bash
# install (first time)
cp .claude/bots/telegram/com.example.telegram.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.example.telegram.plist

# status
launchctl list | grep sheero

# view logs (live)
tail -f ~/Library/Logs/sheero-telegram.log

# restart after code change
launchctl kickstart -k gui/$(id -u)/com.example.telegram

# stop / uninstall
launchctl unload ~/Library/LaunchAgents/com.example.telegram.plist
rm ~/Library/LaunchAgents/com.example.telegram.plist
```

## Dependencies

Managed by `uv` in a local `.venv/`:

```bash
cd .claude/bots/telegram
uv sync   # creates .venv, installs python-telegram-bot
```

Python ≥ 3.11 (uv will fetch one if your system doesn't have it).

## Limits & safeguards

- **Whitelist:** hard owner ID check; rejections logged with offender's Telegram ID
- **Rate limit:** 10 messages / minute per user (token bucket, in-memory)
- **Daily cost cap:** `DAILY_COST_CAP_USD` (default $5). Bot stops invoking Claude when hit; resumes next day
- **Cost tracking:** approximate — uses `usage.input_tokens`/`output_tokens` from Claude's JSON output at Sonnet rates ($3/M input, $15/M output)

## State files (NOT in repo)

- `~/.config/sheero/sessions.json` — Telegram user ID → Claude session ID
- `~/.config/sheero/daily_spend.json` — date → spend (last 30 days, auto-pruned)
- `~/Library/Logs/sheero-telegram.log` — daemon stdout/stderr

## Troubleshooting

- **No reply from bot**: check `tail -f ~/Library/Logs/sheero-telegram.log`. Common: expired OAuth token, rate limit, daily cap, `claude` not on PATH for launchd.
- **launchd keeps restarting**: it's the `KeepAlive` config. Fix the underlying crash first. `launchctl unload` during diagnosis to stop the loop.
- **Claude calls error**: run the exact command manually from the brain dir: `claude -p "hi" --output-format json`. If that errors, the bot will too.
- **Daily cap too tight/loose**: edit `DAILY_COST_CAP_USD` in the env file, then `launchctl kickstart -k ...`.
