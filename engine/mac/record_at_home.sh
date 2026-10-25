#!/bin/bash
# Mac recorder, started by hand (Scott's choice, 25 Oct 2026): double-click "Record Morning Briefing" on the Desktop,
# or run: bash ~/MorningBriefing/podcastmemory/engine/mac/record_at_home.sh [YYYY-MM-DD]
# Waits for the cloud run (9:29pm the evening before) to save the script to GitHub, then records it with Fish Audio S2-Pro
# in the reference voice from engine/mac/voice.json: the full episode, with chapter markers.
# (No headlines edition; removed 25 Oct 2026.) Saves the MP3 and the answer sheet to iCloud Drive > Morning Briefing, with a notification.
# If Fish fails, records the episode with the show's Kokoro voice instead.
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
BASE="$HOME/MorningBriefing"; REPO="$BASE/podcastmemory"
# The episode is for the coming morning: tomorrow's date in the evening, today's if run after midnight (by hand).
if [ -n "$1" ]; then DATE="$1"
elif [ "$(TZ=Australia/Sydney date +%H)" -ge 12 ]; then DATE="$(TZ=Australia/Sydney date -v+1d +%F)"; else DATE="$(TZ=Australia/Sydney date +%F)"; fi
STARTED=$(date +%s); Y="${DATE:0:4}"; M="${DATE:5:2}"
EP="$REPO/archive/$Y/$M/$DATE"
DEST="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Morning Briefing"
OUT="$HOME/podcast/out"
MP3="$OUT/Morning_Briefing_$DATE.mp3"
notify() { osascript -e "display notification \"$1\" with title \"Morning Briefing\"" >/dev/null 2>&1 || true; }
echo "== $(date) waiting for the $DATE script"
caffeinate -is -w $$ &

while :; do
  git -C "$REPO" pull -q --rebase --autostash || true
  [ -f "$EP/script/11_chat_outro.txt" ] && break
  if [ $(( $(date +%s) - STARTED )) -ge 14400 ]; then echo "no script after 4 hours, giving up"; notify "No script arrived tonight"; exit 0; fi
  sleep 120
done
sleep 30; git -C "$REPO" pull -q --rebase --autostash || true
mkdir -p "$DEST"
cp "$EP/sheet.txt" "$DEST/Sheet_$DATE.txt" 2>/dev/null || true

# record: Fish first, the Kokoro voice if that fails. Non-zero if nothing was made.
record() {
  rm -f "$MP3"
  "$BASE/fish/bin/python" "$REPO/engine/mac/build_fish.py" "$DATE" && [ -s "$MP3" ] && return 0
  echo "Fish failed, recording with the Kokoro voice instead"
  ESPEAK_NG="$(brew --prefix)/bin/espeak-ng" PATH="$BASE/venv/bin:$PATH" sh "$REPO/engine/build_episode.sh" "$DATE"
}

echo "== $(date) recording the full episode"
record || { echo "recording failed"; notify "Recording failed this morning; the script is in the Claude app"; exit 1; }
cp "$MP3" "$DEST/"
notify "Today's full episode is in iCloud Drive > Morning Briefing"
echo "== $(date) saved to $DEST"
