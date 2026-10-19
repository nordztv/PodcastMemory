#!/bin/bash
# Softer, sweeter voice audition (default model VoxCPM2; pass another model ID as the first argument).
# Reads the audition passage with soft and sweet reference clips of the show's voice (more of the breathy
# Nicole blend, a touch of Bella or Sky, a little slower, warmer EQ), each also with a gentle "soft finish".
# Run after voice_audition.sh:  bash ~/MorningBriefing/podcastmemory/engine/mac/soft_audition.sh
# Results: ~/MorningBriefing/audition_soft/  (softness 1 = slightly softer ... 3 = softest)
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
BASE="$HOME/MorningBriefing"; REPO="$BASE/podcastmemory"; OUT="$BASE/audition_soft"
GEN="$BASE/mlx/bin/mlx_audio.tts.generate"; MODEL="${1:-mlx-community/VoxCPM2-8bit}"
git -C "$REPO" pull -q || true
[ -x "$GEN" ] || { echo "Run voice_audition.sh first (it installs mlx-audio)."; exit 1; }
mkdir -p "$OUT"; cd "$OUT"
TEXT="Good morning Scott, I hope you are doing well today. Right, the news first, and I'll be honest, Canberra has outdone itself again. A committee was formed to review why there are too many committees. You can't make it up. Anyway, in much happier news, Final Fantasy Resonance lands on Wednesday, and I know exactly what you'll be doing at lunch. Don't pretend otherwise. I see you."
SOFT="lowshelf=f=220:g=1.5,equalizer=f=3500:t=q:w=1.2:g=-3,highshelf=f=7000:g=-4,deesser,acompressor=threshold=-22dB:ratio=2.5:attack=15:release=200"

for ref in soft1 soft2 soft3 sweet1 sweet2 sweet3; do
  echo "=== $ref"
  REF_TEXT="$(cat "$REPO/engine/mac/ref_${ref%[0-9]}.txt")"
  args=(--model "$MODEL" --text "$TEXT" --output_path "$OUT" --file_prefix "v_$ref" --join_audio --ref_audio "$REPO/engine/mac/ref_$ref.wav")
  "$GEN" "${args[@]}" --ref_text "$REF_TEXT" >"v_$ref.log" 2>&1 || "$GEN" "${args[@]}" >"v_$ref.log" 2>&1 || { echo "failed, see v_$ref.log"; continue; }
  f=$(ls -t v_$ref*.wav | head -1)
  ffmpeg -loglevel error -y -i "$f" -b:a 128k "${ref}.mp3"
  ffmpeg -loglevel error -y -i "$f" -af "$SOFT" -b:a 128k "${ref}_plus_soft_finish.mp3"
  rm -f "$f"
done
echo "Done. Tell Claude which file you like best."
open "$OUT"
