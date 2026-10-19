# Recording on the MacBook Pro (VoxCPM2 voice)

Scott chose VoxCPM2 (cloned from the show's Heart clip, `heart_reference.wav`) as the show's voice. It runs on the Mac's Apple silicon, so the Mac is the main recorder:

- The cloud run (1:45am) writes the script and saves it to GitHub, and still sends its own Kokoro recording in the Claude app as a backup.
- At 3:25am on weekdays the Mac wakes; at 3:30 it waits for the script, records it with VoxCPM2 (`build_voxcpm.py`), and saves the MP3 and workout sheet to iCloud Drive > Morning Briefing, with a notification.
- If VoxCPM2 fails, it records with the Kokoro voice instead (unless the cloud already delivered).

The Mac needs to be plugged in overnight (it can wake with the lid closed only on power).

## One-time setup

1. Install Homebrew if you don't have it: https://brew.sh
2. In Terminal (skip the first two lines if already done):
   ```
   brew install gh && gh auth login
   mkdir -p ~/MorningBriefing && gh repo clone nordztv/PodcastMemory ~/MorningBriefing/podcastmemory
   bash ~/MorningBriefing/podcastmemory/engine/mac/install.sh
   ```

## Handy commands

- Record any day by hand: `~/MorningBriefing/venv/bin/python ~/MorningBriefing/podcastmemory/engine/mac/build_voxcpm.py 2026-10-20` (MP3 lands in `~/podcast/out/`)
- Log: `~/MorningBriefing/record.log`
- Voice auditions: `voice_audition.sh`, `soft_audition.sh`
- Turn it off: `launchctl unload ~/Library/LaunchAgents/com.scott.morningbriefing.plist` and `sudo pmset repeat cancel`
