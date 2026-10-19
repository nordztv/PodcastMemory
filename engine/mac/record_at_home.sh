#!/bin/bash
# Main recorder, run on Scott's MacBook Pro at 3:30am on weekdays (set up by install.sh).
# Waits for the cloud run to save today's script to GitHub (it starts 1:45am), then records with VoxCPM2
# (Scott's chosen voice): the five-minute headlines edition first, then the full episode (with chapter markers).
# Saves the MP3s and workout sheet to iCloud Drive > Morning Briefing, and, if engine/mac/jellyfin_setup.sh has
# been run, also copies the MP3s into the Jellyfin folder on the home server, with a notification.
# The cloud still sends its own Kokoro recording in the Claude app as a backup.
# If VoxCPM2 fails, records with the Kokoro voice here instead, unless the cloud already delivered.
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
BASE="$HOME/MorningBriefing"; REPO="$BASE/podcastmemory"
DATE="$(TZ=Australia/Sydney date +%F)"; Y="${DATE:0:4}"; M="${DATE:5:2}"
EP="$REPO/archive/$Y/$M/$DATE"
DEST="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Morning Briefing"
OUT="$HOME/podcast/out"
MP3="$OUT/Morning_Briefing_$DATE.mp3"
HL="$OUT/Morning_Briefing_${DATE}_headlines.mp3"
echo "== $(date) waiting for the $DATE script"
caffeinate -is -w $$ &

while :; do
  git -C "$REPO" pull -q || true
  [ -f "$EP/script/11_chat_outro.txt" ] && break
  if [ "$(TZ=Australia/Sydney date +%H%M)" -ge 0530 ]; then echo "no script by 5:30, giving up"; exit 0; fi
  sleep 120
done
sleep 30; git -C "$REPO" pull -q || true
mkdir -p "$DEST"

# Copies one finished MP3 to iCloud Drive and, when set up, the Jellyfin folder on the home server.
deliver() {
  cp "$1" "$DEST/"
  if [ -f "$BASE/jellyfin.conf" ]; then
    . "$BASE/jellyfin.conf"   # JELLYFIN_SMB (e.g. smb://truenas.local/media) and JELLYFIN_DIR (folder under /Volumes)
    share="/Volumes/$(basename "$JELLYFIN_SMB")"
    [ -d "$share" ] || osascript -e "mount volume \"$JELLYFIN_SMB\"" >/dev/null 2>&1 || true
    if [ -d "$share" ] && mkdir -p "$JELLYFIN_DIR" && cp "$1" "$JELLYFIN_DIR/"; then
      echo "copied $(basename "$1") to Jellyfin"
    else
      echo "Jellyfin share not reachable, skipped $(basename "$1")"
    fi
  fi
}

# record <headlines|full>: VoxCPM2 first, Kokoro if that fails. Returns non-zero if nothing was made.
record() {
  local mode="$1" out="$MP3" arg=""
  [ "$mode" = headlines ] && { out="$HL"; arg=headlines; }
  rm -f "$out"
  "$BASE/venv/bin/python" "$REPO/engine/mac/build_voxcpm.py" "$DATE" $arg && return 0
  git -C "$REPO" pull -q || true
  if [ "$mode" = full ] && [ -f "$EP/delivered.txt" ]; then
    echo "VoxCPM2 failed; the cloud already sent today's episode in the Claude app"
    osascript -e 'display notification "VoxCPM2 failed this morning; the episode is in the Claude app" with title "Morning Briefing"' || true
    return 1
  fi
  echo "VoxCPM2 failed ($mode), recording with the Kokoro voice instead"
  ESPEAK_NG="$(brew --prefix)/bin/espeak-ng" PATH="$BASE/venv/bin:$PATH" sh "$REPO/engine/build_episode.sh" "$DATE" $arg
}

if [ -d "$EP/headlines" ]; then
  echo "== $(date) recording the headlines edition"
  if record headlines; then
    deliver "$HL"
    osascript -e "display notification \"The five-minute headlines are ready; the full episode is on its way\" with title \"Morning Briefing\"" || true
  else
    echo "headlines recording failed"
  fi
fi

echo "== $(date) recording the full episode with VoxCPM2"
record full || { echo "recording failed"; exit 1; }
deliver "$MP3"
cp "$EP/workout.txt" "$DEST/Workout_$DATE.txt" 2>/dev/null || true
osascript -e "display notification \"Today's episode is in iCloud Drive > Morning Briefing\" with title \"Morning Briefing is ready\"" || true
echo "== $(date) saved to $DEST"
