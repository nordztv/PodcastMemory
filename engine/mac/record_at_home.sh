#!/bin/bash
# Mac recording has been retired (Scott's choice, 20 Oct 2026); episodes are recorded in the cloud only.
# The Mac's old 3:30am schedule still points at this file, so it now just switches that schedule off, once.
PLIST="$HOME/Library/LaunchAgents/com.scott.morningbriefing.plist"
echo "== $(date) Mac recording retired; turning off the 3:30am schedule"
osascript -e 'display notification "Mac recording is now off. To stop the 3:25am wake too, run in Terminal: sudo pmset repeat cancel" with title "Morning Briefing"' || true
rm -f "$PLIST"
launchctl remove com.scott.morningbriefing 2>/dev/null || true
exit 0
