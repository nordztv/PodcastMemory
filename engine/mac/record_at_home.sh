#!/bin/bash
# Mac recorder, started by hand: double-click the Record shortcut on the Desktop,
# or run: bash ~/MorningBriefing/podcastmemory/engine/mac/record_at_home.sh [YYYY-MM-DD] [am|pm|eve|quick]
# Voices one of Mizuki's calls in her Kokoro voice (the same engine the cloud uses), with chapter markers, from the
# script the cloud run saved to GitHub:  am = the morning call (written at about 3am),
# pm = the walk-home call (written about 2pm that day), eve = the weekend's 7pm call.
# No arguments: it picks the call that is due next by Sydney time (see below). "quick": the first part only.
# Saves the MP3 to iCloud Drive > Mizuki, with a notification. Sets up anything missing on its first run.
set -e
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
BASE="$HOME/MorningBriefing"; REPO="$BASE/podcastmemory"
DATE=""; MODE=""; CALL=""
for a in "$@"; do case "$a" in am|pm|eve) CALL="$a";; quick) MODE=quick;; *) DATE="$a";; esac; done
H=$((10#$(TZ=Australia/Sydney date +%H))); TODAY="$(TZ=Australia/Sydney date +%F)"; TOMORROW="$(TZ=Australia/Sydney date -v+1d +%F)"
if [ -z "$DATE" ]; then
  DOW=$(TZ=Australia/Sydney date +%u)   # 1 = Monday ... 6 = Saturday, 7 = Sunday
  PICK=""
  if [ "$DOW" = 6 ]; then DATE="$TODAY"; PICK=eve                      # Saturday: tonight's 7pm call
  elif [ "$DOW" = 7 ] && [ "$H" -lt 20 ]; then DATE="$TODAY"; PICK=eve  # Sunday before 8pm: tonight's call
  elif [ "$DOW" = 7 ]; then DATE="$TOMORROW"; PICK=am                   # Sunday night: Monday morning's call (written about 3am)
  elif [ "$H" -lt 12 ]; then DATE="$TODAY"; PICK=am                     # weekday morning: this morning's call
  elif [ "$H" -lt 21 ] || [ "$DOW" = 5 ]; then DATE="$TODAY"; PICK=pm   # weekday afternoon and evening: today's 4pm call
  else DATE="$TOMORROW"; PICK=am; fi                                    # late weekday night: tomorrow's morning call (written about 3am)
  CALL="${CALL:-$PICK}"
fi
if [ -z "$CALL" ]; then   # a date was given without am/pm/eve: weekend dates have one call, weekdays default to the morning
  if [ "$(date -j -f %F "$DATE" +%u)" -ge 6 ]; then CALL=eve; else CALL=am; fi
fi
# The call's files are am_*, pm_* or eve_* (any number of parts); days before 16 Nov 2026 used fixed names.
case "$CALL" in am) OLD="06_japan.txt"; NAME="morning_call";;
                pm) OLD="11_chat_outro.txt"; NAME="walk_home_call";;
                eve) OLD="05_evening_goodbye.txt"; NAME="evening_call";; esac
have_script() { ls "$EP/script/${CALL}_"*.txt >/dev/null 2>&1 || [ -f "$EP/script/$OLD" ]; }
first_part() { ls "$EP/script/${CALL}_"*.txt 2>/dev/null | sort | head -1; }
STARTED=$(date +%s); Y="${DATE:0:4}"; M="${DATE:5:2}"
EP="$REPO/archive/$Y/$M/$DATE"
DEST="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Mizuki"
OUT="$HOME/podcast/out"
notify() { osascript -e "display notification \"$1\" with title \"Mizuki\"" >/dev/null 2>&1 || true; }
# One at a time (two double-clicks could overlap); a lock older than 6 hours is stale.
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

echo "== $(date) waiting for the $DATE $CALL script ${MODE:+($MODE)}"
while :; do
  git -C "$REPO" pull -q --rebase --autostash || true
  have_script && break
  if [ $(( $(date +%s) - STARTED )) -ge 36000 ]; then echo "no script after 10 hours, giving up"; notify "No script for that call arrived"; exit 0; fi
  sleep 120
done
sleep 30; git -C "$REPO" pull -q --rebase --autostash || true

setup || { notify "Recording setup failed; see the Terminal window"; exit 1; }
export ESPEAK_NG="$(command -v espeak-ng)"
export PATH="$BASE/venv/bin:$PATH"
mkdir -p "$DEST" "$OUT"

if [ "$MODE" = "quick" ]; then
  MP3="$OUT/Mizuki_${DATE}_sample.mp3"
  echo "== $(date) voicing the first part only"
  FIRST="$(first_part)"; [ -n "$FIRST" ] || FIRST="$(ls "$EP"/script/0*.txt | sort | head -1)"
  python3 "$REPO/engine/tts.py" "$FIRST" "$MP3" || { notify "Recording failed"; exit 1; }
else
  MP3="$OUT/Mizuki_${DATE}_$NAME.mp3"
  rm -rf "$HOME/podcast/render/${DATE}_$CALL" "$MP3"   # fresh render of the current script
  echo "== $(date) voicing the $CALL call"
  sh "$REPO/engine/build_episode.sh" "$DATE" "$CALL" || { echo "recording failed"; notify "Voicing the call failed; the script is in the Claude app"; exit 1; }
fi
cp "$MP3" "$DEST/"
notify "Mizuki's call is in iCloud Drive > Mizuki"
echo "== $(date) saved to $DEST"
