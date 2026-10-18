#!/bin/sh
# Builds one episode MP3 from its script sections.
# Usage: sh engine/build_episode.sh YYYY-MM-DD
# Reads archive/YYYY/MM/YYYY-MM-DD/script/NN_*.txt in order, renders two sections at a time,
# joins them with 1.8 s gaps and writes ~/podcast/out/Morning_Briefing_YYYY-MM-DD.mp3 (64 kbps mono).
set -e
D="$1"; [ -n "$D" ] || { echo "usage: build_episode.sh YYYY-MM-DD"; exit 1; }
REPO="$(cd "$(dirname "$0")/.." && pwd)"
Y=$(echo "$D" | cut -c1-4); M=$(echo "$D" | cut -c6-7)
SRC="$REPO/archive/$Y/$M/$D/script"
WORK="$HOME/podcast/render/$D"; OUT="$HOME/podcast/out"
mkdir -p "$WORK" "$OUT"
ls "$SRC"/*.txt >/dev/null

ls "$SRC"/*.txt | xargs -P2 -I{} sh -c 'f="{}"; b=$(basename "$f" .txt); [ -s "'"$WORK"'/$b.mp3" ] || python3 "'"$REPO"'/engine/tts.py" "$f" "'"$WORK"'/$b.mp3"'

ffmpeg -loglevel error -y -f lavfi -i anullsrc=r=24000:cl=mono -t 1.8 -b:a 128k "$WORK/gap.mp3"
: > "$WORK/list.txt"
for f in $(ls "$SRC"/*.txt); do
  echo "file '$WORK/$(basename "$f" .txt).mp3'" >> "$WORK/list.txt"
  echo "file '$WORK/gap.mp3'" >> "$WORK/list.txt"
done
ffmpeg -loglevel error -y -f concat -safe 0 -i "$WORK/list.txt" -ar 24000 -ac 1 -b:a 64k \
  -metadata title="Morning Briefing - $D" -metadata artist="Morning Briefing" "$OUT/Morning_Briefing_$D.mp3"
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$OUT/Morning_Briefing_$D.mp3"
