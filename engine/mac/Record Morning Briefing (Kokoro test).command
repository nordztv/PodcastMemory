#!/bin/bash
# Double-click to record the Morning Briefing in the Kokoro voice (a test, for comparing with Fish).
# Saves Morning_Briefing_DATE_kokoro.mp3 to iCloud Drive > Morning Briefing. The Fish recording is never touched.
# In the evening it records the next morning's episode; before noon, today's. Leave this window open until it says it's saved.
git -C "$HOME/MorningBriefing/podcastmemory" pull -q --rebase --autostash || true
bash "$HOME/MorningBriefing/podcastmemory/engine/mac/record_kokoro.sh" "$@" 2>&1 | tee -a "$HOME/MorningBriefing/record_kokoro.log"
echo; echo "Finished. You can close this window."
