#!/bin/sh
# Builds one episode MP3 from its script sections.
# Usage: sh engine/build_episode.sh YYYY-MM-DD [headlines]
# Full episode: reads archive/YYYY/MM/YYYY-MM-DD/script/NN_*.txt in order, renders two sections at a time,
# joins them with 1.8 s gaps and writes ~/podcast/out/Morning_Briefing_YYYY-MM-DD.mp3 (96 kbps mono, light warm "Happy 1" EQ),
# with a chapter marker per section (engine/chapters.py).
# "headlines": the five-minute edition from archive/.../headlines/*.txt -> ~/podcast/out/Morning_Briefing_YYYY-MM-DD_headlines.mp3
set -e
D="$1"; [ -n "$D" ] || { echo "usage: build_episode.sh YYYY-MM-DD [headlines]"; exit 1; }
MODE="$2"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
Y=$(echo "$D" | cut -c1-4); M=$(echo "$D" | cut -c6-7)
OUT="$HOME/podcast/out"
if [ "$MODE" = "headlines" ]; then
  SRC="$REPO/archive/$Y/$M/$D/headlines"; WORK="$HOME/podcast/render/${D}_headlines"; MP3="$OUT/Morning_Briefing_${D}_headlines.mp3"
else
  SRC="$REPO/archive/$Y/$M/$D/script"; WORK="$HOME/podcast/render/$D"; MP3="$OUT/Morning_Briefing_$D.mp3"
fi
mkdir -p "$WORK" "$OUT"
ls "$SRC"/*.txt >/dev/null

ls "$SRC"/*.txt | xargs -P2 -I{} sh -c 'f="{}"; b=$(basename "$f" .txt); [ -s "'"$WORK"'/$b.mp3" ] || python3 "'"$REPO"'/engine/tts.py" "$f" "'"$WORK"'/$b.mp3"'

GAP=1.8
ffmpeg -loglevel error -y -f lavfi -i anullsrc=r=24000:cl=mono -t $GAP -b:a 128k "$WORK/gap.mp3"
: > "$WORK/list.txt"; : > "$WORK/timings.txt"
for f in $(ls "$SRC"/*.txt); do
  b=$(basename "$f" .txt)
  echo "file '$WORK/$b.mp3'" >> "$WORK/list.txt"
  echo "file '$WORK/gap.mp3'" >> "$WORK/list.txt"
  len=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$WORK/$b.mp3")
  printf '%s\t%s\n' "$b" "$(python3 -c "print($len + $GAP)")" >> "$WORK/timings.txt"
done
ffmpeg -loglevel error -y -f concat -safe 0 -i "$WORK/list.txt" -af "lowshelf=f=220:g=1,equalizer=f=3500:t=q:w=1.2:g=-1.5,highshelf=f=7000:g=-2,deesser" -ar 24000 -ac 1 -b:a 96k \
  -metadata title="Morning Briefing - $D" -metadata artist="Morning Briefing" "$MP3"
python3 "$REPO/engine/chapters.py" "$MP3" "$WORK/timings.txt" "$D" $MODE || echo "chapters skipped (episode is fine without them)"
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$MP3"
