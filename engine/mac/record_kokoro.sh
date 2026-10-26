#!/bin/bash
# Kokoro test recorder for the Mac (Scott's request, 27 Oct 2026): records an episode in the show's Kokoro voice
# (the same voice the cloud uses) instead of Fish, so the two can be compared. It never touches the Fish recording.
#
#   bash ~/MorningBriefing/podcastmemory/engine/mac/record_kokoro.sh [YYYY-MM-DD] [quick]
#
# No date: tomorrow's episode in the evening, today's before noon (same rule as record_at_home.sh).
# "quick": records only the opening section (a few minutes), handy for a fast listen.
# Output: ~/podcast/out/Morning_Briefing_DATE_kokoro.mp3 (or _kokoro_sample.mp3), also copied to
# iCloud Drive > Morning Briefing and opened when done. Safe to run again; sets up anything missing on the first run.
set -e
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
BASE="$HOME/MorningBriefing"; REPO="$BASE/podcastmemory"
if [ -n "$1" ] && [ "$1" != "quick" ]; then DATE="$1"; MODE="$2"; else MODE="$1"
  if [ "$(TZ=Australia/Sydney date +%H)" -ge 12 ]; then DATE="$(TZ=Australia/Sydney date -v+1d +%F)"; else DATE="$(TZ=Australia/Sydney date +%F)"; fi
fi
Y="${DATE:0:4}"; M="${DATE:5:2}"; EP="$REPO/archive/$Y/$M/$DATE"
OUT="$HOME/podcast/out"; DEST="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Morning Briefing"
notify() { osascript -e "display notification \"$1\" with title \"Morning Briefing\"" >/dev/null 2>&1 || true; }
caffeinate -dims -w $$ &

echo "== $(date) Kokoro test for $DATE ${MODE:+($MODE)}"
git -C "$REPO" pull -q --rebase --autostash || true
[ -f "$EP/script/01_opening_world.txt" ] || { echo "No script for $DATE on GitHub yet. Try again once it's there."; exit 1; }

# One-time bits (skipped when already there): tools, the Kokoro Python environment and the voice files.
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
  || { echo "Voice files failed their checksum; delete ~/tts and run again."; exit 1; }

export ESPEAK_NG="$(command -v espeak-ng)"
export PATH="$BASE/venv/bin:$PATH"
mkdir -p "$OUT" "$DEST"

if [ "$MODE" = "quick" ]; then
  MP3="$OUT/Morning_Briefing_${DATE}_kokoro_sample.mp3"
  echo "== recording the opening section only"
  python3 "$REPO/engine/tts.py" "$EP/script/01_opening_world.txt" "$MP3"
else
  MAIN="$OUT/Morning_Briefing_$DATE.mp3"; KEEP="$OUT/.fish_keep_$DATE.mp3"
  [ -f "$MAIN" ] && mv "$MAIN" "$KEEP"                       # keep any Fish recording safe
  trap '[ -f "$KEEP" ] && mv "$KEEP" "$MAIN"' EXIT
  rm -rf "$HOME/podcast/render/$DATE"                        # fresh Kokoro render of the current script
  echo "== recording the full episode (roughly as long as the episode itself, depending on the Mac)"
  sh "$REPO/engine/build_episode.sh" "$DATE"
  MP3="$OUT/Morning_Briefing_${DATE}_kokoro.mp3"
  mv "$MAIN" "$MP3"
fi

cp "$MP3" "$DEST/"
notify "Kokoro test saved to iCloud Drive > Morning Briefing"
echo "== $(date) saved: $MP3 (and in iCloud Drive > Morning Briefing)"
open "$MP3" || true
