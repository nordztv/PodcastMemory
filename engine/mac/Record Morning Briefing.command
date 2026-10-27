#!/bin/bash
# Double-click to record the Morning Briefing in the show's Kokoro voice and save it to iCloud Drive > Morning Briefing.
# In the evening it records the next morning's episode; before noon, today's. Leave this window open until it says it's saved.
git -C "$HOME/MorningBriefing/podcastmemory" pull -q --rebase --autostash || true
bash "$HOME/MorningBriefing/podcastmemory/engine/mac/record_at_home.sh" 2>&1 | tee -a "$HOME/MorningBriefing/record.log"
echo; echo "Finished. You can close this window."
