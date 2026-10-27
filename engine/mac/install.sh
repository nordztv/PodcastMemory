#!/bin/bash
# One-time setup of Morning Briefing home recording on Scott's MacBook Pro, in the show's Kokoro voice
# (Kokoro only since 27 Oct 2026, Scott's choice; this also removes the old Fish Audio setup).
# Run in Terminal:  bash ~/MorningBriefing/podcastmemory/engine/mac/install.sh
# Needs Homebrew (https://brew.sh). Safe to run again.
set -e
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
BASE="$HOME/MorningBriefing"
REPO="$BASE/podcastmemory"
mkdir -p "$BASE" && cd "$BASE"

echo "1/4 Tools (ffmpeg, espeak-ng, Python) and the Kokoro voice environment"
brew install ffmpeg espeak-ng python@3.12 >/dev/null
PY="$(brew --prefix python@3.12)/bin/python3.12"
[ -x "$BASE/venv/bin/python" ] || "$PY" -m venv "$BASE/venv"
"$BASE/venv/bin/pip" install -q --upgrade pip numpy onnxruntime
ln -sf "$BASE/venv/bin/python" "$BASE/venv/bin/python3"

echo "2/4 Voice files (from the repo's own backup, checked against its checksums)"
git -C "$REPO" pull -q --rebase --autostash
git -C "$REPO" sparse-checkout add voice_backup 2>/dev/null || true
mkdir -p "$HOME/tts"
for f in kokoro-v1.0.onnx voices-v1.0.bin; do
  [ -s "$HOME/tts/$f" ] || cat "$REPO"/voice_backup/"$f".part* > "$HOME/tts/$f"
done
(cd "$HOME/tts" && grep -E " (kokoro-v1.0.onnx|voices-v1.0.bin)\$" "$REPO/voice_backup/SHA256SUMS" | shasum -a 256 -c -)

echo "3/4 Removing the old Fish Audio setup (its Python environment and downloaded models), if present"
rm -rf "$BASE/fish" "$HOME/podcast/render_fish"
for d in "$HOME"/.cache/huggingface/hub/models--*fish-audio-s2-pro*; do [ -e "$d" ] && rm -rf "$d" && echo "   removed $d"; done
rm -f "$HOME/Desktop/Record Morning Briefing (Kokoro test).command"

echo "4/4 Desktop shortcut and a quick voice test"
cp "$REPO/engine/mac/Record Morning Briefing.command" "$HOME/Desktop/" && chmod +x "$HOME/Desktop/Record Morning Briefing.command"
echo "[happy] Good morning Scott, I hope you are doing well today. The home studio is ready." > "$BASE/voice_test.txt"
ESPEAK_NG="$(command -v espeak-ng)" PATH="$BASE/venv/bin:$PATH" python3 "$REPO/engine/tts.py" "$BASE/voice_test.txt" "$BASE/voice_test.mp3"
open "$BASE/voice_test.mp3"

echo "Done. To record an episode, double-click \"Record Morning Briefing\" on your Desktop."
echo "   Episodes appear in iCloud Drive > Morning Briefing."
