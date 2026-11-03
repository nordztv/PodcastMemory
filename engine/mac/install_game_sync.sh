#!/bin/bash
# One-time setup of the weekly game-project sync on Scott's MacBook Pro (3 Nov 2026).
# Run in Terminal:  bash ~/MorningBriefing/podcastmemory/engine/mac/install_game_sync.sh [path to Game-Prototype]
# Installs a launchd job that runs sync_game_project.sh every Sunday at 7:30pm (if the Mac is asleep then,
# it runs when it wakes), adds a "Sync Game Project" shortcut to the Desktop, and does a first sync now.
set -e
BASE="$HOME/MorningBriefing"; REPO="$BASE/podcastmemory"; CONF="$BASE/game_sync.conf"
mkdir -p "$BASE" "$HOME/Library/LaunchAgents"
if [ -n "$1" ]; then
  [ -f "$1/project.godot" ] || { echo "No project.godot in $1"; exit 1; }
  grep -v '^GAME_DIR=' "$CONF" 2>/dev/null > "$CONF.tmp" || true; echo "GAME_DIR=\"$1\"" >> "$CONF.tmp"; mv "$CONF.tmp" "$CONF"
fi
PLIST="$HOME/Library/LaunchAgents/com.morningbriefing.gamesync.plist"
cat > "$PLIST" <<PL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.morningbriefing.gamesync</string>
  <key>ProgramArguments</key><array><string>/bin/bash</string><string>$REPO/engine/mac/sync_game_project.sh</string></array>
  <key>StartCalendarInterval</key><dict><key>Weekday</key><integer>0</integer><key>Hour</key><integer>19</integer><key>Minute</key><integer>30</integer></dict>
  <key>StandardOutPath</key><string>$BASE/game_sync.log</string>
  <key>StandardErrorPath</key><string>$BASE/game_sync.log</string>
</dict></plist>
PL
launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"
cp "$REPO/engine/mac/Sync Game Project.command" "$HOME/Desktop/" && chmod +x "$HOME/Desktop/Sync Game Project.command"
echo "Installed: every Sunday at 7:30pm your game project is synced for the week's episodes."
echo "Running the first sync now..."
bash "$REPO/engine/mac/sync_game_project.sh"
