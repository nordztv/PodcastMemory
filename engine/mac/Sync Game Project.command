#!/bin/bash
# Double-click to send your Game-Prototype project's current weekly task and notes to the Morning Briefing.
git -C "$HOME/MorningBriefing/podcastmemory" pull -q --rebase --autostash || true
bash "$HOME/MorningBriefing/podcastmemory/engine/mac/sync_game_project.sh" 2>&1 | tee -a "$HOME/MorningBriefing/game_sync.log"
echo; echo "Finished. You can close this window."
