#!/bin/sh
# Installs the Morning Briefing voice engine into ~/tts and ~/dl/piper.
# Tries the backup copies in this repo's "voice-engine-v1" release first, then the original upstream links.
# Needs: python3 with numpy + onnxruntime, ffmpeg (normally preinstalled). PyPI is usually blocked; GitHub works.
set -e
mkdir -p "$HOME/tts" "$HOME/dl/piper"

fetch() { # fetch <file> <upstream url> <dest dir>
  [ -s "$3/$1" ] && return 0
  gh release download voice-engine-v1 -R nordztv/podcastmemory -p "$1" -D "$3" --clobber 2>/dev/null \
    || curl -sSL --fail -o "$3/$1" "$2"
}

fetch kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx "$HOME/tts"
fetch voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin "$HOME/tts"
fetch piper.tgz https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz "$HOME/dl/piper"
[ -x "$HOME/dl/piper/piper/espeak-ng" ] || (cd "$HOME/dl/piper" && tar xzf piper.tgz && chmod +x piper/espeak-ng)

python3 -c "import numpy, onnxruntime" || { echo "numpy/onnxruntime missing"; exit 1; }
command -v ffmpeg >/dev/null || { echo "ffmpeg missing"; exit 1; }
ls -la "$HOME/tts" "$HOME/dl/piper/piper/espeak-ng"
echo "Voice engine ready."
