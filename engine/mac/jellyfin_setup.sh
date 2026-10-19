#!/bin/bash
# One-time setup: also deliver each Morning Briefing MP3 into a folder on the home server that Jellyfin watches,
# so episodes show up in Jellyfin (and its phone apps) as an album called "Morning Briefing".
# Run in Terminal:  bash ~/MorningBriefing/podcastmemory/engine/mac/jellyfin_setup.sh
# Safe to run again (it just rewrites ~/MorningBriefing/jellyfin.conf). To turn it off: rm ~/MorningBriefing/jellyfin.conf
set -e
BASE="$HOME/MorningBriefing"
echo "Address of the server share Jellyfin's media lives on, e.g. smb://truenas.local/media"
read -r -p "Share: " SMB
SMB="${SMB%/}"
echo "Folder inside that share for the show (created if missing), e.g. Podcasts/Morning Briefing"
read -r -p "Folder [Podcasts/Morning Briefing]: " SUB
SUB="${SUB:-Podcasts/Morning Briefing}"
SHARE="/Volumes/$(basename "$SMB")"
echo "Connecting once (tick 'Remember this password in my keychain' if asked, so the 3:30am run can reconnect)..."
[ -d "$SHARE" ] || osascript -e "mount volume \"$SMB\""
[ -d "$SHARE" ] || { echo "Couldn't connect to $SMB. Check the address and try again."; exit 1; }
mkdir -p "$SHARE/$SUB"
printf 'JELLYFIN_SMB=%q\nJELLYFIN_DIR=%q\n' "$SMB" "$SHARE/$SUB" > "$BASE/jellyfin.conf"
ls "$HOME/Library/Mobile Documents/com~apple~CloudDocs/Morning Briefing/"*.mp3 2>/dev/null | tail -5 | while read -r f; do cp "$f" "$SHARE/$SUB/"; done
echo "Done. New episodes will be copied to $SHARE/$SUB each morning (the last few were copied now)."
echo "In Jellyfin: Dashboard > Libraries > Add Media Library, type Music, folder = that folder as the server sees it"
echo "(for example /mnt/media/Podcasts/Morning Briefing). Episodes appear as the album 'Morning Briefing'."
