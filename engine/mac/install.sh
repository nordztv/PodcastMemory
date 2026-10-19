#!/bin/bash
# One-time setup of Morning Briefing home recording on Scott's MacBook Pro.
# Run in Terminal:  bash ~/MorningBriefing/podcastmemory/engine/mac/install.sh
# Needs Homebrew (https://brew.sh). Safe to run again.
set -e
BASE="$HOME/MorningBriefing"
REPO="$BASE/podcastmemory"
cd "$BASE"

echo "1/5 Tools (ffmpeg, espeak-ng, Python packages)"
brew install ffmpeg espeak-ng python@3.12 >/dev/null
PY="$(brew --prefix python@3.12)/bin/python3.12"
"$PY" -m venv "$BASE/venv"
"$BASE/venv/bin/pip" install -q --upgrade pip numpy onnxruntime

echo "2/5 Voice model (from the repo's own backup, checked against its checksums)"
git -C "$REPO" pull -q
mkdir -p "$HOME/tts"
for f in kokoro-v1.0.onnx voices-v1.0.bin; do
  if [ ! -s "$HOME/tts/$f" ]; then cat "$REPO"/voice_backup/"$f".part* > "$HOME/tts/$f"; fi
done
(cd "$HOME/tts" && grep -E " (kokoro-v1.0.onnx|voices-v1.0.bin)\$" "$REPO/voice_backup/SHA256SUMS" | shasum -a 256 -c -)

echo "3/5 Voice test"
echo "Good morning Scott, the home studio is ready." > "$BASE/test.txt"
ESPEAK_NG="$(brew --prefix)/bin/espeak-ng" "$BASE/venv/bin/python" "$REPO/engine/tts.py" "$BASE/test.txt" "$BASE/test.mp3"
open "$BASE/test.mp3"

echo "4/5 Schedule (weekdays 5:00am, plus wake the Mac at 4:58am)"
PLIST="$HOME/Library/LaunchAgents/com.scott.morningbriefing.plist"
mkdir -p "$HOME/Library/LaunchAgents"
cat > "$PLIST" <<PL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.scott.morningbriefing</string>
  <key>ProgramArguments</key><array><string>/bin/bash</string><string>$REPO/engine/mac/record_at_home.sh</string></array>
  <key>StartCalendarInterval</key><array>
$(for d in 1 2 3 4 5; do echo "    <dict><key>Weekday</key><integer>$d</integer><key>Hour</key><integer>5</integer><key>Minute</key><integer>0</integer></dict>"; done)
  </array>
  <key>StandardOutPath</key><string>$BASE/record.log</string>
  <key>StandardErrorPath</key><string>$BASE/record.log</string>
</dict></plist>
PL
launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"
echo "   Your Mac password is needed once, to let it wake itself at 4:58am on weekdays:"
sudo pmset repeat wakeorpoweron MTWRF 04:58:00

echo "5/5 Done. Episodes recorded at home will appear in iCloud Drive > Morning Briefing."
