#!/bin/sh
# Builds one day's calls MP3 from its script sections.
# Usage: sh engine/build_episode.sh YYYY-MM-DD [am|pm|eve]
# Full day's calls: reads archive/YYYY/MM/YYYY-MM-DD/script/NN_*.txt in order, renders two sections at a time,
# joins them with 0.7 s gaps and writes ~/podcast/out/Mizuki_YYYY-MM-DD.mp3 (96 kbps mono, light warm "Happy 1" EQ),
# with a chapter marker per section (engine/chapters.py).
# "am": only parts 01 to 06 (the morning call)   -> ~/podcast/out/Mizuki_YYYY-MM-DD_morning_call.mp3
# "eve": the weekend's single 7pm call (01_evening_* to 05_evening_*) -> ~/podcast/out/Mizuki_YYYY-MM-DD_evening_call.mp3
# "pm": only parts 07 to 11 (the walk-home call) -> ~/podcast/out/Mizuki_YYYY-MM-DD_walk_home_call.mp3
# "headlines": the five-minute edition from archive/.../headlines/*.txt -> ~/podcast/out/Mizuki_YYYY-MM-DD_headlines.mp3
set -e
D="$1"; [ -n "$D" ] || { echo "usage: build_episode.sh YYYY-MM-DD [am|pm|eve]"; exit 1; }
MODE="$2"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
Y=$(echo "$D" | cut -c1-4); M=$(echo "$D" | cut -c6-7)
OUT="$HOME/podcast/out"
if [ "$MODE" = "headlines" ]; then
  SRC="$REPO/archive/$Y/$M/$D/headlines"; WORK="$HOME/podcast/render/${D}_headlines"; MP3="$OUT/Mizuki_${D}_headlines.mp3"
else
  SRC="$REPO/archive/$Y/$M/$D/script"; WORK="$HOME/podcast/render/$D"; MP3="$OUT/Mizuki_$D.mp3"
fi
PARTS='*'
if [ "$MODE" = "am" ]; then PARTS='0[1-6]_*'; WORK="$HOME/podcast/render/${D}_am"; MP3="$OUT/Mizuki_${D}_morning_call.mp3"; fi
if [ "$MODE" = "eve" ]; then PARTS='0[1-5]_evening_*'; WORK="$HOME/podcast/render/${D}_eve"; MP3="$OUT/Mizuki_${D}_evening_call.mp3"; fi
if [ "$MODE" = "pm" ]; then PARTS='0[7-9]_* 1[0-9]_*'; WORK="$HOME/podcast/render/${D}_pm"; MP3="$OUT/Mizuki_${D}_walk_home_call.mp3"; fi
mkdir -p "$WORK" "$OUT"
# set -f while $PARTS is split into patterns, so a pattern is matched in $SRC and never in the current directory
files() { set -f; for g in $PARTS; do set +f; ls "$SRC"/$g.txt 2>/dev/null; set -f; done; set +f; }
[ -n "$(files)" ] || { echo "no script files for $D $MODE"; exit 1; }

# -n1 with the file as $1 (not -I{}): macOS xargs caps -I commands at 255 bytes ("command line cannot be assembled")
# Her energy that day (1 to 10) colours the voice: the Energy table in memory/mizuki_life.md has a row per date.
MB_ENERGY=$(grep -E "^\| $D \| [0-9]+ \|" "$REPO/memory/mizuki_life.md" | head -1 | cut -d'|' -f3 | tr -d ' ')
[ -n "$MB_ENERGY" ] || MB_ENERGY=6
echo "Energy for the voice: $MB_ENERGY of 10"
export WORK REPO MB_ENERGY MIZUKI_MUSIC
# Each part: the voice only (tts.py). It's a phone call, so there is no music (Scott, 13 Nov 2026); MIZUKI_MUSIC=1
# brings back the old mood music under spooky and secret moments (engine/music.py).
files | xargs -P2 -n1 sh -c 'f="$1"; b=$(basename "$f" .txt); [ -s "$WORK/$b.mp3" ] || { [ -s "$WORK/$b.voice.mp3" ] || python3 "$REPO/engine/tts.py" "$f" "$WORK/$b.voice.mp3"; { [ "$MIZUKI_MUSIC" = 1 ] && python3 "$REPO/engine/music.py" "$WORK/$b.voice.mp3" "$WORK/$b.mp3"; } || cp "$WORK/$b.voice.mp3" "$WORK/$b.mp3"; }' _

GAP=0.7   # short, so the day's calls flows as one phone call (Scott, 11 Nov 2026; was 1.8)
ffmpeg -loglevel error -y -f lavfi -i anullsrc=r=24000:cl=mono -t $GAP -b:a 128k "$WORK/gap.mp3"
: > "$WORK/list.txt"; : > "$WORK/timings.txt"
for f in $(files); do
  b=$(basename "$f" .txt)
  echo "file '$WORK/$b.mp3'" >> "$WORK/list.txt"
  echo "file '$WORK/gap.mp3'" >> "$WORK/list.txt"
  len=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$WORK/$b.mp3")
  printf '%s\t%s\n' "$b" "$(python3 -c "print($len + $GAP)")" >> "$WORK/timings.txt"
done
ffmpeg -loglevel error -y -f concat -safe 0 -i "$WORK/list.txt" -af "lowshelf=f=220:g=1,equalizer=f=3500:t=q:w=1.2:g=-1.5,highshelf=f=7000:g=-2,deesser" -ar 24000 -ac 1 -b:a 96k \
  -metadata title="Mizuki - $D${MODE:+ ($MODE)}" -metadata artist="Mizuki" "$MP3"
python3 "$REPO/engine/chapters.py" "$MP3" "$WORK/timings.txt" "$D" $MODE || echo "chapters skipped (day's calls is fine without them)"
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$MP3"
