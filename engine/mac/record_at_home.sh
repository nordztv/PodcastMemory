#!/bin/bash
# Main recorder, run on Scott's MacBook Pro at 3:30am on weekdays (set up by install.sh).
# Waits for the cloud run to save today's script to GitHub (it starts 1:45am), then records the episode with
# VoxCPM2 (Scott's chosen voice) and saves the MP3 and workout sheet to iCloud Drive > Morning Briefing.
# The cloud still sends its own Kokoro recording in the Claude app as a backup.
# If VoxCPM2 fails, records with the Kokoro voice here instead, unless the cloud already delivered.
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
BASE="$HOME/MorningBriefing"; REPO="$BASE/podcastmemory"
DATE="$(TZ=Australia/Sydney date +%F)"; Y="${DATE:0:4}"; M="${DATE:5:2}"
EP="$REPO/archive/$Y/$M/$DATE"
DEST="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Morning Briefing"
MP3="$HOME/podcast/out/Morning_Briefing_$DATE.mp3"
echo "== $(date) waiting for the $DATE script"
caffeinate -is -w $$ &

while :; do
  git -C "$REPO" pull -q || true
  [ -f "$EP/script/11_chat_outro.txt" ] && break
  if [ "$(TZ=Australia/Sydney date +%H%M)" -ge 0530 ]; then echo "no script by 5:30, giving up"; exit 0; fi
  sleep 120
done
sleep 30; git -C "$REPO" pull -q || true

echo "== $(date) recording with VoxCPM2"
rm -f "$MP3"
if ! "$BASE/venv/bin/python" "$REPO/engine/mac/build_voxcpm.py" "$DATE"; then
  git -C "$REPO" pull -q || true
  if [ -f "$EP/delivered.txt" ]; then
    echo "VoxCPM2 failed; the cloud already sent today's episode in the Claude app"
    osascript -e 'display notification "VoxCPM2 failed this morning; the episode is in the Claude app" with title "Morning Briefing"' || true
    exit 1
  fi
  echo "VoxCPM2 failed, recording with the Kokoro voice instead"
  ESPEAK_NG="$(brew --prefix)/bin/espeak-ng" PATH="$BASE/venv/bin:$PATH" sh "$REPO/engine/build_episode.sh" "$DATE" || { echo "recording failed"; exit 1; }
fi
mkdir -p "$DEST"
cp "$MP3" "$DEST/"
cp "$EP/workout.txt" "$DEST/Workout_$DATE.txt" 2>/dev/null || true
osascript -e "display notification \"Today's episode is in iCloud Drive > Morning Briefing\" with title \"Morning Briefing is ready\"" || true
echo "== $(date) saved to $DEST"
