#!/bin/bash
# Softer Higgs Audio v2: reads the audition passage with three softer reference clips of the show's voice
# (more of the breathy Nicole blend, a little slower, warmer EQ), each also with a gentle "soft finish".
# Run after voice_audition.sh:  bash ~/MorningBriefing/podcastmemory/engine/mac/soft_audition.sh
# Results: ~/MorningBriefing/audition_soft/  (softness 1 = slightly softer ... 3 = softest)
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
BASE="$HOME/MorningBriefing"; REPO="$BASE/podcastmemory"; OUT="$BASE/audition_soft"
GEN="$BASE/mlx/bin/mlx_audio.tts.generate"; MODEL=mlx-community/higgs-audio-v2-3B-mlx-q8
git -C "$REPO" pull -q || true
[ -x "$GEN" ] || { echo "Run voice_audition.sh first (it installs mlx-audio)."; exit 1; }
mkdir -p "$OUT"; cd "$OUT"
REF_TEXT="$(cat "$REPO/engine/mac/ref_soft.txt")"
TEXT="Good morning Scott, I hope you are doing well today. Right, the news first, and I'll be honest, Canberra has outdone itself again. A committee was formed to review why there are too many committees. You can't make it up. Anyway, in much happier news, Final Fantasy Resonance lands on Wednesday, and I know exactly what you'll be doing at lunch. Don't pretend otherwise. I see you."
SOFT="lowshelf=f=220:g=1.5,equalizer=f=3500:t=q:w=1.2:g=-3,highshelf=f=7000:g=-4,deesser,acompressor=threshold=-22dB:ratio=2.5:attack=15:release=200"

for n in 1 2 3; do
  echo "=== softness $n"
  args=(--model "$MODEL" --text "$TEXT" --output_path "$OUT" --file_prefix "higgs_soft$n" --join_audio --ref_audio "$REPO/engine/mac/ref_soft$n.wav")
  "$GEN" "${args[@]}" --ref_text "$REF_TEXT" >"higgs_soft$n.log" 2>&1 || "$GEN" "${args[@]}" >"higgs_soft$n.log" 2>&1 || { echo "failed, see higgs_soft$n.log"; continue; }
  f=$(ls -t higgs_soft$n*.wav | head -1)
  ffmpeg -loglevel error -y -i "$f" -b:a 128k "Softness_${n}.mp3"
  ffmpeg -loglevel error -y -i "$f" -af "$SOFT" -b:a 128k "Softness_${n}_plus_soft_finish.mp3"
  rm -f "$f"
done
echo "Done. Tell Claude which file you like best."
open "$OUT"
