#!/bin/bash
# Mac recorder, started by hand (Scott's choice, 25 Oct 2026): double-click "Record Morning Briefing" on the Desktop,
# or run: bash ~/MorningBriefing/podcastmemory/engine/mac/record_at_home.sh [YYYY-MM-DD] [quick]
# Records the episode in the show's Kokoro voice (Scott's choice, 27 Oct 2026: Kokoro only, Fish removed), the same voice
# the cloud uses, with chapter markers. Waits for the cloud run (about 9:30pm the evening before) to save the script to GitHub.
# No date: tomorrow's episode in the evening, today's before noon. "quick": the opening section only, for a fast listen.
# Saves the MP3 and the answer sheet to iCloud Drive > Morning Briefing, with a notification. Sets up anything missing on its first run.
set -e
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
BASE="$HOME/MorningBriefing"; REPO="$BASE/podcastmemory"
if [ -n "$1" ] && [ "$1" != "quick" ]; then DATE="$1"; MODE="$2"; else MODE="$1"
  if [ "$(TZ=Australia/Sydney date +%H)" -ge 12 ]; then DATE="$(TZ=Australia/Sydney date -v+1d +%F)"; else DATE="$(TZ=Australia/Sydney date +%F)"; fi
fi
STARTED=$(date +%s); Y="${DATE:0:4}"; M="${DATE:5:2}"
EP="$REPO/archive/$Y/$M/$DATE"
DEST="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Morning Briefing"
OUT="$HOME/podcast/out"
notify() { osascript -e "display notification \"$1\" with title \"Morning Briefing\"" >/dev/null 2>&1 || true; }
# One recording at a time (the 9:40pm automatic one and a double-click could overlap); a lock older than 6 hours is stale.
LOCK="$BASE/.recording.lock"
if ! mkdir "$LOCK" 2>/dev/null; then
  if [ -n "$(find "$LOCK" -maxdepth 0 -mmin +360 2>/dev/null)" ]; then rm -rf "$LOCK"; mkdir "$LOCK"
  else echo "A recording is already running (see ~/MorningBriefing/record.log). Nothing to do."; exit 0; fi
fi
trap 'rm -rf "$LOCK"' EXIT
caffeinate -dims -w $$ &

# One-time bits (skipped when already there): tools, the Python environment and the Kokoro voice files from the repo's backup.
setup() {
  command -v ffmpeg >/dev/null && command -v espeak-ng >/dev/null || brew install ffmpeg espeak-ng
  if [ ! -x "$BASE/venv/bin/python" ]; then
    brew list python@3.12 >/dev/null 2>&1 || brew install python@3.12
    "$(brew --prefix python@3.12)/bin/python3.12" -m venv "$BASE/venv"
  fi
  "$BASE/venv/bin/python" -c "import numpy, onnxruntime" 2>/dev/null || "$BASE/venv/bin/pip" install -q --upgrade pip numpy onnxruntime
  ln -sf "$BASE/venv/bin/python" "$BASE/venv/bin/python3"
  mkdir -p "$HOME/tts"
  for f in kokoro-v1.0.onnx voices-v1.0.bin; do
    if [ ! -s "$HOME/tts/$f" ]; then
      git -C "$REPO" sparse-checkout add voice_backup 2>/dev/null || true
      cat "$REPO"/voice_backup/"$f".part* > "$HOME/tts/$f"
    fi
  done
  (cd "$HOME/tts" && grep -E " (kokoro-v1.0.onnx|voices-v1.0.bin)\$" "$REPO/voice_backup/SHA256SUMS" | shasum -a 256 -c - >/dev/null) \
    || { echo "Voice files failed their checksum; delete ~/tts and run again."; return 1; }
}

echo "== $(date) waiting for the $DATE script ${MODE:+($MODE)}"
while :; do
  git -C "$REPO" pull -q --rebase --autostash || true
  [ -f "$EP/script/11_chat_outro.txt" ] && break
  if [ $(( $(date +%s) - STARTED )) -ge 14400 ]; then echo "no script after 4 hours, giving up"; notify "No script arrived tonight"; exit 0; fi
  sleep 120
done
sleep 30; git -C "$REPO" pull -q --rebase --autostash || true

setup || { notify "Recording setup failed; see the Terminal window"; exit 1; }
export ESPEAK_NG="$(command -v espeak-ng)"
export PATH="$BASE/venv/bin:$PATH"
mkdir -p "$DEST" "$OUT"
cp "$EP/sheet.txt" "$DEST/Sheet_$DATE.txt" 2>/dev/null || true

if [ "$MODE" = "quick" ]; then
  MP3="$OUT/Morning_Briefing_${DATE}_sample.mp3"
  echo "== $(date) recording the opening section only"
  python3 "$REPO/engine/tts.py" "$EP/script/01_opening_world.txt" "$MP3" || { notify "Recording failed"; exit 1; }
else
  MP3="$OUT/Morning_Briefing_$DATE.mp3"
  rm -rf "$HOME/podcast/render/$DATE" "$MP3"   # fresh render of the current script
  echo "== $(date) recording the full episode"
  sh "$REPO/engine/build_episode.sh" "$DATE" || { echo "recording failed"; notify "Recording failed this morning; the script is in the Claude app"; exit 1; }
fi
cp "$MP3" "$DEST/"
notify "Today's episode is in iCloud Drive > Morning Briefing"
echo "== $(date) saved to $DEST"
