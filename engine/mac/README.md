# Home recording on the MacBook Pro

A backup for mornings when the cloud run can't record the audio. At 5:00am on weekdays the Mac wakes, checks GitHub, and:
- does nothing if the cloud delivered the episode;
- records it if the cloud left the script but no audio (or nothing was delivered by 5:45am);
- saves the MP3 and workout sheet to iCloud Drive > Morning Briefing, then shows a notification.

The Mac needs to be plugged in (it can wake from sleep with the lid closed only on power). Recording takes about 10 to 20 minutes.

## One-time setup (about 15 minutes)

1. Install Homebrew if you don't have it: https://brew.sh (paste the one line it shows into Terminal).
2. In Terminal:
   ```
   brew install gh && gh auth login
   mkdir -p ~/MorningBriefing && gh repo clone nordztv/PodcastMemory ~/MorningBriefing/podcastmemory
   bash ~/MorningBriefing/podcastmemory/engine/mac/install.sh
   ```
   `gh auth login`: choose GitHub.com, HTTPS, and log in with a browser. The install asks for your Mac password once (to schedule the 4:58am wake-up) and plays a short voice test when it's done.

## Checking on it

- Log: `~/MorningBriefing/record.log`
- Record a day by hand: `ESPEAK_NG=$(brew --prefix)/bin/espeak-ng PATH=~/MorningBriefing/venv/bin:$PATH sh ~/MorningBriefing/podcastmemory/engine/build_episode.sh 2026-10-20`
- Turn it off: `launchctl unload ~/Library/LaunchAgents/com.scott.morningbriefing.plist` and `sudo pmset repeat cancel`
