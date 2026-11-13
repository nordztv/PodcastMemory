#!/bin/bash
# Double-click to voice Mizuki's next call in her Kokoro voice and save it to iCloud Drive > Mizuki.
# It picks the call that's due by Sydney time: the morning call, the 4pm walk-home call, or the weekend's 7pm call.
# Leave this window open until it says it's saved.
git -C "$HOME/MorningBriefing/podcastmemory" pull -q --rebase --autostash || true
bash "$HOME/MorningBriefing/podcastmemory/engine/mac/record_at_home.sh" "$@" 2>&1 | tee -a "$HOME/MorningBriefing/record.log"
echo; echo "Finished. You can close this window."
