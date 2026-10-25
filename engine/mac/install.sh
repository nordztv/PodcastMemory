#!/bin/bash
# One-time setup of Morning Briefing home recording (Fish Audio S2-Pro) on Scott's MacBook Pro.
# Run in Terminal:  bash ~/MorningBriefing/podcastmemory/engine/mac/install.sh
# Needs Homebrew (https://brew.sh). Safe to run again.
set -e
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
BASE="$HOME/MorningBriefing"
REPO="$BASE/podcastmemory"
mkdir -p "$BASE" && cd "$BASE"

echo "1/5 Tools (ffmpeg, espeak-ng, Python, mlx-audio for Fish S2-Pro)"
brew install ffmpeg espeak-ng python@3.12 >/dev/null
PY="$(brew --prefix python@3.12)/bin/python3.12"
[ -x "$BASE/fish/bin/python" ] || "$PY" -m venv "$BASE/fish"
"$BASE/fish/bin/pip" install -q --upgrade pip mlx-audio
# Backup voice (Kokoro), used only if Fish fails
[ -x "$BASE/venv/bin/python" ] || "$PY" -m venv "$BASE/venv"
"$BASE/venv/bin/pip" install -q --upgrade pip numpy onnxruntime
ln -sf "$BASE/venv/bin/python" "$BASE/venv/bin/python3"

echo "2/5 Backup voice files (from the repo's own backup, checked against its checksums)"
git -C "$REPO" pull -q
mkdir -p "$HOME/tts"
for f in kokoro-v1.0.onnx voices-v1.0.bin; do
  [ -s "$HOME/tts/$f" ] || cat "$REPO"/voice_backup/"$f".part* > "$HOME/tts/$f"
done
(cd "$HOME/tts" && grep -E " (kokoro-v1.0.onnx|voices-v1.0.bin)\$" "$REPO/voice_backup/SHA256SUMS" | shasum -a 256 -c -)

echo "3/5 Fish voice test (downloads the model, about 7 GB, the first time)"
TESTDIR="$REPO/archive/2000/01/2000-01-01/headlines"; mkdir -p "$TESTDIR"
echo "Good morning Scott, I hope you are doing well today. The home studio is ready." > "$TESTDIR/01_headlines.txt"
"$BASE/fish/bin/python" "$REPO/engine/mac/build_fish.py" 2000-01-01 headlines
rm -rf "$REPO/archive/2000"
open "$HOME/podcast/out/Morning_Briefing_2000-01-01_headlines.mp3"

echo "4/5 Schedule (weekdays 1:05am, plus wake the Mac at 1:00am)"
PLIST="$HOME/Library/LaunchAgents/com.scott.morningbriefing.plist"
mkdir -p "$HOME/Library/LaunchAgents"
cat > "$PLIST" <<PL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.scott.morningbriefing</string>
  <key>ProgramArguments</key><array><string>/bin/bash</string><string>$REPO/engine/mac/record_at_home.sh</string></array>
  <key>StartCalendarInterval</key><array>
$(for d in 1 2 3 4 5; do echo "    <dict><key>Weekday</key><integer>$d</integer><key>Hour</key><integer>1</integer><key>Minute</key><integer>5</integer></dict>"; done)
  </array>
  <key>StandardOutPath</key><string>$BASE/record.log</string>
  <key>StandardErrorPath</key><string>$BASE/record.log</string>
</dict></plist>
PL
launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"
echo "   Your Mac password is needed once, to let it wake itself at 1:00am on weekdays:"
sudo pmset repeat wakeorpoweron MTWRF 01:00:00

echo "5/5 Done. Episodes will appear in iCloud Drive > Morning Briefing."
echo "   Next, run the speed test to see how long a full episode takes on this Mac:"
echo "   bash $REPO/engine/mac/speed_test.sh"
