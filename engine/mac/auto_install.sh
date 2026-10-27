#!/bin/bash
# Turns on automatic recording (Scott's request, 27 Oct 2026): every Sunday to Thursday at 9:40pm the Mac waits for the
# night's script, records it in the Kokoro voice and saves it to iCloud Drive > Morning Briefing.
#   bash ~/MorningBriefing/podcastmemory/engine/mac/auto_install.sh          turn it on
#   bash ~/MorningBriefing/podcastmemory/engine/mac/auto_install.sh off      turn it off
# Optional: it can also set the Mac to wake itself at 9:38pm on those nights (asks for your Mac password once).
# Run install.sh first if you haven't. Safe to run again.
set -e
BASE="$HOME/MorningBriefing"; REPO="$BASE/podcastmemory"
LABEL="com.scott.morningbriefing"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"

if [ "$1" = "off" ]; then
  launchctl bootout "gui/$(id -u)" "$PLIST" 2>/dev/null || launchctl unload "$PLIST" 2>/dev/null || true
  rm -f "$PLIST"
  if pmset -g sched 2>/dev/null | grep -qi "wakeorpoweron"; then echo "Your Mac password is needed to cancel the automatic wake-up:"; sudo pmset repeat cancel; fi
  echo "Automatic recording is off. Double-click Record Morning Briefing on the Desktop to record by hand."
  exit 0
fi

chmod +x "$REPO/engine/mac/auto_record.sh"
mkdir -p "$HOME/Library/LaunchAgents"
{
  echo '<?xml version="1.0" encoding="UTF-8"?>'
  echo '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">'
  echo '<plist version="1.0"><dict>'
  echo "  <key>Label</key><string>$LABEL</string>"
  echo "  <key>ProgramArguments</key><array><string>/bin/bash</string><string>$REPO/engine/mac/auto_record.sh</string></array>"
  echo '  <key>StartCalendarInterval</key><array>'
  for wd in 0 1 2 3 4; do echo "    <dict><key>Weekday</key><integer>$wd</integer><key>Hour</key><integer>21</integer><key>Minute</key><integer>40</integer></dict>"; done
  echo '  </array>'
  echo "  <key>StandardOutPath</key><string>$BASE/record.log</string>"
  echo "  <key>StandardErrorPath</key><string>$BASE/record.log</string>"
  echo '</dict></plist>'
} > "$PLIST"
launchctl bootout "gui/$(id -u)" "$PLIST" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST" 2>/dev/null || launchctl load "$PLIST"
echo "Automatic recording is on: Sunday to Thursday at 9:40pm (this Mac's clock), saved to iCloud Drive > Morning Briefing."
echo "Log: $BASE/record.log"

read -r -p "Also wake the Mac at 9:38pm on those nights if it's asleep? (needs your Mac password) [y/N] " yn
if [ "$yn" = "y" ] || [ "$yn" = "Y" ]; then
  sudo pmset repeat wakeorpoweron SMTWR 21:38:00 && echo "Wake-up set. Keep it plugged in; on battery with the lid closed it may not record."
else
  echo "No wake-up set: the Mac needs to be awake at 9:40pm (if it's asleep, the recording starts when it next wakes)."
fi
