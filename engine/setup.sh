#!/bin/sh
# Installs the Morning Briefing voice engine into ~/tts and ~/dl/piper.
# Tries the original upstream links first (fast); if they fail, rebuilds the files from this repo's
# voice_backup/ folder (split into parts) and checks them against voice_backup/SHA256SUMS.
# Needs: python3 with numpy + onnxruntime, ffmpeg (normally preinstalled). PyPI is usually blocked; GitHub works.
set -e
REPO="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$HOME/tts" "$HOME/dl/piper"

from_backup() { # from_backup <file> <dest dir>
  git -C "$REPO" sparse-checkout add voice_backup 2>/dev/null || true
  cat "$REPO"/voice_backup/"$1".part* > "$2/$1"
  (cd "$2" && grep " $1\$" "$REPO/voice_backup/SHA256SUMS" | sha256sum -c -)
}

fetch() { # fetch <file> <upstream url> <dest dir>
  [ -s "$3/$1" ] && return 0
  curl -sSL --fail -o "$3/$1" "$2" || { echo "upstream failed for $1, using repo backup"; from_backup "$1" "$3"; }
}

fetch kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx "$HOME/tts"
fetch voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin "$HOME/tts"
fetch piper.tgz https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz "$HOME/dl/piper"
[ -x "$HOME/dl/piper/piper/espeak-ng" ] || (cd "$HOME/dl/piper" && tar xzf piper.tgz && chmod +x piper/espeak-ng)

python3 -c "import numpy, onnxruntime" || { echo "numpy/onnxruntime missing"; exit 1; }
command -v ffmpeg >/dev/null || { echo "ffmpeg missing"; exit 1; }
echo "Voice engine ready."
