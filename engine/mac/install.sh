#!/bin/bash
# One-time setup of Morning Briefing home recording on Scott's MacBook Pro.
# Run in Terminal:  bash ~/MorningBriefing/podcastmemory/engine/mac/install.sh
# Needs Homebrew (https://brew.sh). Safe to run again.
set -e
BASE="$HOME/MorningBriefing"
REPO="$BASE/podcastmemory"
cd "$BASE"

echo "1/5 Tools (ffmpeg, espeak-ng, Python packages, mlx-audio for VoxCPM2)"
brew install ffmpeg espeak-ng python@3.12 >/dev/null
PY="$(brew --prefix python@3.12)/bin/python3.12"
"$PY" -m venv "$BASE/venv"
"$BASE/venv/bin/pip" install -q --upgrade pip numpy onnxruntime
[ -x "$BASE/mlx/bin/mlx_audio.tts.generate" ] || { "$PY" -m venv "$BASE/mlx" && "$BASE/mlx/bin/pip" install -q --upgrade pip mlx-audio; }

echo "2/5 Voice model (from the repo's own backup, checked against its checksums)"
git -C "$REPO" pull -q
mkdir -p "$HOME/tts"
for f in kokoro-v1.0.onnx voices-v1.0.bin; do
  if [ ! -s "$HOME/tts/$f" ]; then cat "$REPO"/voice_backup/"$f".part* > "$HOME/tts/$f"; fi
done
(cd "$HOME/tts" && grep -E " (kokoro-v1.0.onnx|voices-v1.0.bin)\$" "$REPO/voice_backup/SHA256SUMS" | shasum -a 256 -c -)

echo "3/5 Voice test (VoxCPM2; downloads the model the first time)"
echo "Good morning Scott, the home studio is ready." > "$BASE/test.txt"
"$BASE/mlx/bin/mlx_audio.tts.generate" --model mlx-community/VoxCPM2-8bit --text "$(cat "$BASE/test.txt")" --ref_audio "$REPO/engine/mac/heart_reference.wav" --output_path "$BASE" --file_prefix test --join_audio
open "$(ls -t "$BASE"/test*.wav | head -1)"

echo "4/5 Schedule (weekdays 3:30am, plus wake the Mac at 3:25am)"
PLIST="$HOME/Library/LaunchAgents/com.scott.morningbriefing.plist"
mkdir -p "$HOME/Library/LaunchAgents"
cat > "$PLIST" <<PL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.scott.morningbriefing</string>
  <key>ProgramArguments</key><array><string>/bin/bash</string><string>$REPO/engine/mac/record_at_home.sh</string></array>
  <key>StartCalendarInterval</key><array>
$(for d in 1 2 3 4 5; do echo "    <dict><key>Weekday</key><integer>$d</integer><key>Hour</key><integer>3</integer><key>Minute</key><integer>30</integer></dict>"; done)
  </array>
  <key>StandardOutPath</key><string>$BASE/record.log</string>
  <key>StandardErrorPath</key><string>$BASE/record.log</string>
</dict></plist>
PL
launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"
echo "   Your Mac password is needed once, to let it wake itself at 3:25am on weekdays:"
sudo pmset repeat wakeorpoweron MTWRF 03:25:00

echo "5/5 Done. Episodes recorded at home will appear in iCloud Drive > Morning Briefing."
