# Recording on the MacBook Pro (Fish Audio S2-Pro)

Set up 25 October 2026 at Scott's request. The cloud run (12:29am weekdays) writes the script and saves it to GitHub. The MacBook Pro then records it in Scott's reference voice with Fish Audio S2-Pro, and saves the audio to iCloud Drive > Morning Briefing.

- 1:00am weekdays: the Mac wakes. 1:05am: `record_at_home.sh` starts and checks GitHub every two minutes for the day's script (it gives up at 6am).
- It records the full episode with chapter markers (`build_fish.py`) and copies the MP3 plus the answer sheet into iCloud Drive > Morning Briefing, with a notification. (No headlines edition.)
- The voice: `voice.json` names the reference clip (`ref_happy1.wav`, "Happy 1") and its transcript (`ref_happy.txt`). To use another voice, add a 10 to 30 second WAV and its exact transcript here and change the two names.
- If Fish fails, the episode is recorded with the show's Kokoro voice instead.
- Fish S2-Pro is free for personal, non-commercial use (Fish Audio Research License).

The Mac must be plugged in overnight (it can wake on schedule with the lid closed only on power).

## One-time setup

1. Install Homebrew if you don't have it: https://brew.sh
2. In Terminal:
   ```
   brew install gh && gh auth login
   mkdir -p ~/MorningBriefing && gh repo clone nordztv/PodcastMemory ~/MorningBriefing/podcastmemory
   bash ~/MorningBriefing/podcastmemory/engine/mac/install.sh
   bash ~/MorningBriefing/podcastmemory/engine/mac/speed_test.sh
   ```
   If `~/MorningBriefing/podcastmemory` already exists, skip the clone line and run `git -C ~/MorningBriefing/podcastmemory pull` instead.

## Handy commands

- Record any day by hand: `~/MorningBriefing/fish/bin/python ~/MorningBriefing/podcastmemory/engine/mac/build_fish.py 2026-10-23` (MP3s land in `~/podcast/out/`)
- Log: `~/MorningBriefing/record.log`
- Turn it off: `launchctl unload ~/Library/LaunchAgents/com.scott.morningbriefing.plist` and `sudo pmset repeat cancel`
