#!/bin/bash
# Automatic Mac recording (Scott's request, 27 Oct 2026): started by launchd at 9:40pm Sunday to Thursday
# (see auto_install.sh). Waits for that night's script on GitHub (up to 4 hours, via record_at_home.sh), records it in
# the Kokoro voice and saves it to iCloud Drive > Morning Briefing. Skips if that episode is already in iCloud, or if a
# recording is already running (record_at_home.sh holds a lock).
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
BASE="$HOME/MorningBriefing"; REPO="$BASE/podcastmemory"
DEST="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Morning Briefing"
DATE="$(TZ=Australia/Sydney date -v+1d +%F)"
[ "$(TZ=Australia/Sydney date +%H)" -lt 12 ] && DATE="$(TZ=Australia/Sydney date +%F)"

[ -s "$DEST/Morning_Briefing_$DATE.mp3" ] && { echo "$(date) $DATE already in iCloud, nothing to do"; exit 0; }
git -C "$REPO" pull -q --rebase --autostash || true
bash "$REPO/engine/mac/record_at_home.sh" "$DATE"
