#!/bin/bash
# Backup recorder, run on Scott's MacBook Pro at 5:00am on weekdays (set up by install.sh).
# Waits until 5:45am for the cloud run. If the cloud delivered the episode (delivered.txt), does nothing.
# If the cloud couldn't record the audio (it saved Morning_Briefing_DATE_script.txt instead),
# or there's a script but nothing was delivered by 5:45am, records it here and saves the MP3 to iCloud Drive.
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
BASE="$HOME/MorningBriefing"; REPO="$BASE/podcastmemory"
DATE="$(TZ=Australia/Sydney date +%F)"; Y="${DATE:0:4}"; M="${DATE:5:2}"
EP="$REPO/archive/$Y/$M/$DATE"
DEST="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Morning Briefing"
echo "== $(date) checking $DATE"
caffeinate -i -w $$ &

while :; do
  git -C "$REPO" pull -q || true
  if [ -f "$EP/delivered.txt" ]; then echo "cloud delivered it, nothing to do"; exit 0; fi
  if [ -f "$EP/Morning_Briefing_${DATE}_script.txt" ]; then echo "cloud couldn't record, recording here"; break; fi
  if [ "$(TZ=Australia/Sydney date +%H%M)" -ge 0545 ]; then
    if ls "$EP"/script/*.txt >/dev/null 2>&1; then echo "nothing delivered by 5:45, recording here"; break; fi
    echo "no script today, nothing to record"; exit 0
  fi
  sleep 120
done

export ESPEAK_NG="$(brew --prefix)/bin/espeak-ng"
PATH="$BASE/venv/bin:$PATH" sh "$REPO/engine/build_episode.sh" "$DATE" || { echo "recording failed"; exit 1; }
mkdir -p "$DEST"
cp "$HOME/podcast/out/Morning_Briefing_$DATE.mp3" "$DEST/"
cp "$EP/workout.txt" "$DEST/Workout_$DATE.txt" 2>/dev/null || true
osascript -e "display notification \"Today's episode is in iCloud Drive > Morning Briefing\" with title \"Morning Briefing recorded at home\"" || true
echo "saved to $DEST"
