#!/bin/bash
# Voice audition on Scott's MacBook Pro (Apple silicon): reads the same short passage with several
# expressive open voice models, timing each, so Scott can pick one by ear.
# Run:  bash ~/MorningBriefing/podcastmemory/engine/mac/voice_audition.sh
# Results: ~/MorningBriefing/audition/  (one file per model, plus timings.txt). Opens the folder when done.
# The cloning models are given a 12-second clip of the show's current Heart voice (heart_reference.wav),
# so they aim for the same voice, just more expressive. First run downloads several GB of models.
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
BASE="$HOME/MorningBriefing"; REPO="$BASE/podcastmemory"; OUT="$BASE/audition"
REF="$REPO/engine/mac/heart_reference.wav"; REF_TEXT="$(cat "$REPO/engine/mac/heart_reference.txt")"
mkdir -p "$OUT"; cd "$OUT"

[ "$(uname -m)" = "arm64" ] || { echo "This needs an Apple silicon Mac (M1 or newer)."; exit 1; }
echo "Mac: $(sysctl -n machdep.cpu.brand_string), $(( $(sysctl -n hw.memsize) / 1073741824 )) GB memory" | tee "$OUT/timings.txt"

if [ ! -x "$BASE/mlx/bin/mlx_audio.tts.generate" ]; then
  echo "Installing mlx-audio (one time)..."
  PY="$(brew --prefix python@3.12 2>/dev/null)/bin/python3.12"; [ -x "$PY" ] || { brew install python@3.12; PY="$(brew --prefix python@3.12)/bin/python3.12"; }
  "$PY" -m venv "$BASE/mlx" && "$BASE/mlx/bin/pip" install -q --upgrade pip mlx-audio
fi
GEN="$BASE/mlx/bin/mlx_audio.tts.generate"

TEXT="Good morning Scott, I hope you are doing well today. Right, the news first, and I'll be honest, Canberra has outdone itself again. A committee was formed to review why there are too many committees. You can't make it up. Anyway, in much happier news, Final Fantasy Resonance lands on Wednesday, and I know exactly what you'll be doing at lunch. Don't pretend otherwise. I see you."
WORDS=$(echo "$TEXT" | wc -w)

try() { # try <name> <model> [extra args...]
  name="$1"; model="$2"; shift 2
  echo; echo "=== $name ($model)"
  start=$(date +%s)
  if "$GEN" --model "$model" --text "$TEXT" --output_path "$OUT" --file_prefix "$name" --join_audio "$@" >"$OUT/$name.log" 2>&1; then
    secs=$(( $(date +%s) - start ))
    f=$(ls -t "$OUT"/"$name"*.wav 2>/dev/null | head -1)
    dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f" 2>/dev/null | cut -d. -f1)
    est=$( [ -n "$dur" ] && [ "$dur" -gt 0 ] && echo "about $(( secs * 85 * 60 / dur / 60 )) min for an 85-min episode (including first-run download)" )
    echo "$name: OK, ${secs}s to make ${dur}s of audio; $est" | tee -a "$OUT/timings.txt"
  else
    echo "$name: FAILED (see $name.log)" | tee -a "$OUT/timings.txt"
    tail -3 "$OUT/$name.log"
  fi
}

clone() { # clone <name> <model>: with the reference transcript, and without it if that flag isn't supported
  try "$1" "$2" --ref_audio "$REF" --ref_text "$REF_TEXT"
  tail -1 "$OUT/timings.txt" | grep -q FAILED && try "$1" "$2" --ref_audio "$REF"
}

# Baseline: today's voice engine model (Kokoro), on the Mac's GPU
try 1_kokoro_heart mlx-community/Kokoro-82M-bf16 --voice af_heart --speed 0.92
# Expressive models, cloning the Heart clip
clone 2_chatterbox mlx-community/chatterbox-fp16
clone 3_voxcpm2 mlx-community/VoxCPM2-8bit
clone 4_higgs_v2 mlx-community/higgs-audio-v2-3B-mlx-q8
clone 5_csm mlx-community/csm-1b
# Expressive preset voice (no cloning)
try 6_qwen3_vivian mlx-community/Qwen3-TTS-12Hz-0.6B-CustomVoice-8bit --voice Vivian --lang_code English

for f in "$OUT"/*.wav; do ffmpeg -loglevel error -y -i "$f" -b:a 128k "${f%.wav}.mp3" && rm "$f"; done
echo; echo "Done. Listen in $OUT and tell Claude which you like best (and paste timings.txt)."
cat "$OUT/timings.txt"
open "$OUT"
