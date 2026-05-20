---
name: meeting_capture
description: Capture a meeting locally via Whisper (no cloud bot, no Meet participant). Records system audio via BlackHole, transcribes with whisper.cpp, writes raw transcript to memory/feeds/meetings/, then summarizes to journal/meetings/ at meeting end. Trigger with "capture meeting", "start meeting", or "record this".
---

# meeting_capture

## Goal

Capture and summarize a meeting locally on your Mac — no Google Meet bot, no cloud transcription service, nothing leaves your machine. Just system audio → local Whisper → markdown.

This is Sheero's answer to OpenHuman's "Meeting Agent." Rather than join the meeting as a participant (which requires virtual cameras, fake mic input, and a real Google account for the bot), this captures *your end* of the audio and processes it locally.

---

## One-time setup (you do this once, before first use)

These steps need a human at the Mac and only need to be done once.

### 1. Install BlackHole (virtual audio driver)

BlackHole is a free macOS audio driver that lets you route system audio into a "virtual microphone" that recording apps can read.

```bash
brew install blackhole-2ch
```

After install, restart the Mac if needed.

### 2. Create a Multi-Output Device in macOS

In **Audio MIDI Setup** (search Spotlight for "Audio MIDI Setup"):
1. Click `+` bottom-left → **Create Multi-Output Device**
2. Check both **BlackHole 2ch** and your normal speakers/headphones
3. Name it "Meeting Capture"

This routes meeting audio to BOTH your ears AND BlackHole simultaneously, so you can hear the call normally while it's also being captured.

When you have a meeting, switch macOS audio output to "Meeting Capture." Switch back to normal speakers when done.

### 3. Install whisper.cpp

Local Whisper for transcription. Free, offline, fast on Apple Silicon.

```bash
brew install whisper-cpp
# Download a model — base.en is a good size/quality tradeoff for English meetings
mkdir -p ~/.config/sheero/whisper-models
cd ~/.config/sheero/whisper-models
curl -L -o ggml-base.en.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin
```

For higher quality (slower): use `ggml-small.en.bin` or `ggml-medium.en.bin` instead.

### 4. Install ffmpeg (audio recording)

```bash
brew install ffmpeg
```

---

## Step 1 — Before the meeting

User says "start meeting" or "capture meeting [with X about Y]." Optionally collects:
- Who the meeting is with (people)
- What it's about (one-line topic)
- Which project it relates to (for topic-tree attribution)

If the user just says "start meeting" without context, ask one question:

> "Brief context — who is this with and roughly what's it about? (or just say 'go' to skip)"

---

## Step 2 — Start recording

Generate a session ID:
```bash
SESSION_ID=$(date +%Y-%m-%d_%H%M%S)
AUDIO_FILE=/tmp/sheero_meeting_${SESSION_ID}.wav
```

Start ffmpeg recording from BlackHole in the background:
```bash
ffmpeg -f avfoundation -i ":BlackHole 2ch" -ar 16000 -ac 1 -y "$AUDIO_FILE" &
RECORDING_PID=$!
echo $RECORDING_PID > /tmp/sheero_meeting_pid
```

Tell the user:
> "Recording started. Audio routing to BlackHole. Switch macOS output to 'Meeting Capture' if not already. Say 'stop meeting' when done."

---

## Step 3 — Wait for stop signal

Sit idle until the user says "stop meeting", "end meeting", or "meeting done."

If the user asks status mid-meeting, report: file size of `$AUDIO_FILE`, elapsed time.

---

## Step 4 — Stop recording and transcribe

```bash
# Kill ffmpeg cleanly
kill -INT $(cat /tmp/sheero_meeting_pid)
sleep 1

# Run whisper.cpp
TRANSCRIPT_FILE="memory/feeds/meetings/${SESSION_ID}_${TOPIC_SLUG}.md"
whisper-cli \
  -m ~/.config/sheero/whisper-models/ggml-base.en.bin \
  -f "$AUDIO_FILE" \
  --output-txt --output-file "/tmp/sheero_meeting_${SESSION_ID}"
```

Read `/tmp/sheero_meeting_${SESSION_ID}.txt` and wrap it in markdown:

```markdown
---
session_id: <session_id>
date: <YYYY-MM-DD>
duration: <approx minutes>
topic: <one-line topic>
with: [<people>]
project: <project slug if relevant>
source: meeting_capture (local Whisper, base.en model)
---

# Meeting — <topic> — <date>

## Raw transcript

<whisper output>

```

Write to `memory/feeds/meetings/<session_id>_<topic-slug>.md`.

---

## Step 5 — Summarize

Read the raw transcript and produce a meeting summary at `journal/meetings/<session_id>_<topic-slug>.md`:

```markdown
---
session_id: <session_id>
date: <YYYY-MM-DD>
duration: <approx minutes>
topic: <one-line topic>
with: [<people>]
project: <project slug>
transcript: ../../memory/feeds/meetings/<session_id>_<topic-slug>.md
---

# Meeting Summary — <topic> — <date>

## TL;DR
<2-3 sentence summary>

## Decisions made
- <decision> — <one-line context>

## Action items
- [ ] <action> (owner: <name>, due: <date if mentioned>)

## Open questions
- <question that came up without an answer>

## Key quotes
> "..." — <speaker>

## Topics referenced
- <project / person / theme>

## Follow-ups for me
- <what your committed to>
```

---

## Step 6 — Update topic trees

If a project was identified in Step 1:
- Append a one-liner to `cortex/projects/<slug>.md` under `## History`
- Run `refresh_topics` for that single project (skip the hotness pass — just refresh the named one)

If specific people were identified:
- Append to each `cortex/people/<name>.md` under `## History`

---

## Step 7 — Clean up

```bash
rm /tmp/sheero_meeting_${SESSION_ID}.wav
rm /tmp/sheero_meeting_${SESSION_ID}.txt
rm /tmp/sheero_meeting_pid
```

Keep the meeting recording? **No** by default — local Whisper is good enough that re-transcription isn't useful, and meeting audio is bulky + sensitive. If the user explicitly says "keep audio," move the WAV to `~/Library/Application Support/sheero/meeting-audio/`.

---

## Step 8 — Report

> "Meeting captured.
> Transcript: `memory/feeds/meetings/<session_id>_<topic-slug>.md`
> Summary: `journal/meetings/<session_id>_<topic-slug>.md`
> [N decisions, N action items, N open questions]
> Updated topic trees: [list]"

---

## Step 9 — Do NOT commit automatically

Same pattern as other sync skills. Commit happens on next `evening_checkin` or `save`.

---

## Edge cases

- **BlackHole not installed** — detect by checking `ffmpeg -f avfoundation -list_devices true -i ""` for "BlackHole." If missing, tell user how to install and abort gracefully.
- **whisper.cpp not installed** — same, with brew install instructions.
- **macOS output not switched to Meeting Capture** — recording will be silent. After Step 4 if the WAV file is < 100KB, warn the user and ask if they want to abort or check audio setup.
- **Meeting with confidential content** — never auto-summarize via cloud LLM if explicitly flagged confidential. Use Claude Code locally instead.
- **Long meeting (>2 hours)** — whisper.cpp can chunk; pass `--max-len` or split the WAV first.
- **Multiple speakers** — whisper.cpp doesn't do speaker diarization. If diarization matters, suggest the user add speaker labels manually in the transcript before summarization.

---

## Tone

The summary should be ruthlessly action-oriented. Action items > decisions > open questions, in that order of prominence. The raw transcript exists for re-reading later; the summary is for *acting* on the meeting.
