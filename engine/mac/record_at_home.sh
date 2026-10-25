#!/bin/bash
# Mac recorder (Scott's choice, 25 Oct 2026). Runs on the MacBook Pro at 1:05am on weekdays (set up by install.sh).
# Waits for the cloud run (starts 12:29am) to save today's script to GitHub, then records it with Fish Audio S2-Pro
# in the reference voice from engine/mac/voice.json: the full episode, with chapter markers.
# (No headlines edition; removed 25 Oct 2026.) Saves the MP3 and the answer sheet to iCloud Drive > Morning Briefing, with a notification.
# If Fish fails, records the episode with the show's Kokoro voice instead.
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
BASE="$HOME/MorningBriefing"; REPO="$BASE/podcastmemory"
DATE="$(TZ=Australia/Sydney date +%F)"; Y="${DATE:0:4}"; M="${DATE:5:2}"
EP="$REPO/archive/$Y/$M/$DATE"
DEST="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Morning Briefing"
OUT="$HOME/podcast/out"
MP3="$OUT/Morning_Briefing_$DATE.mp3"
notify() { osascript -e "display notification \"$1\" with title \"Morning Briefing\"" >/dev/null 2>&1 || true; }
echo "== $(date) waiting for the $DATE script"
caffeinate -is -w $$ &

while :; do
  git -C "$REPO" pull -q || true
  [ -f "$EP/script/11_chat_outro.txt" ] && break
  if [ "$(TZ=Australia/Sydney date +%H%M)" -ge 0600 ]; then echo "no script by 6am, giving up"; notify "No script arrived this morning"; exit 0; fi
  sleep 120
done
sleep 30; git -C "$REPO" pull -q || true
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
