# Voicing Mizuki's calls on the MacBook Pro (Kokoro voice)

The cloud runs write what Mizuki says on each call and save it to GitHub, and normally voice it too. The MacBook Pro can voice any call itself in the same Kokoro voice, and saves the audio to iCloud Drive > Mizuki. Use it when a cloud run says the voice engine was blocked, or whenever you like.

- There is no schedule: run the one command below in Terminal, or double-click **Record Mizuki Call** on the Desktop. With nothing else typed it picks the call that's due by Sydney time: on a weekday morning that morning's call, in the afternoon the 4pm walk-home call, until 9pm that day's 4pm call, late at night the next morning's call (written about 3am), and on Saturday and Sunday the 7pm call. If that call's script isn't on GitHub yet, it checks every two minutes for up to 10 hours. Leave the Terminal window open (and the Mac plugged in) until it says it's saved.
- It voices the call with chapter markers (`engine/build_episode.sh`, the same build the cloud uses) and copies the MP3 into iCloud Drive > Mizuki, with a notification.
- The voice, its moods and her daily energy are set in `engine/tts.py` (shared with the cloud), so a `git pull` gives the Mac the same improvements.
- It keeps the Mac awake while it works, but closing the lid on battery will pause it.

## One-time setup

1. Install Homebrew if you don't have it: https://brew.sh
2. In Terminal:
   ```
   brew install gh && gh auth login
   mkdir -p ~/MorningBriefing && gh repo clone nordztv/PodcastMemory ~/MorningBriefing/podcastmemory
   bash ~/MorningBriefing/podcastmemory/engine/mac/install.sh
   ```
   If `~/MorningBriefing/podcastmemory` already exists, skip the clone line and run `git -C ~/MorningBriefing/podcastmemory pull` instead. `install.sh` also removes the old Fish Audio setup (its Python environment and downloaded models) if it's there.

## The one command

```
git -C ~/MorningBriefing/podcastmemory pull -q; caffeinate -dims bash ~/MorningBriefing/podcastmemory/engine/mac/record_at_home.sh
```

It sets up anything missing, waits for the script if it isn't on GitHub yet, voices the call that's due and saves it to iCloud Drive > Mizuki.

## Weekly game-project sync (3 Nov 2026)

Mizuki's Friday check-in on your game follows your Game-Prototype weekly task. One-time setup (after the setup above):
```
git -C ~/MorningBriefing/podcastmemory pull -q; bash ~/MorningBriefing/podcastmemory/engine/mac/install_game_sync.sh ~/path/to/Game-Prototype
```
Leave off the path if the folder is in your home, Documents, Developer, Projects, Desktop or GitHub folder (it finds it), or if it's on GitHub as nordztv/Game-Prototype (it clones a copy). It then syncs every Sunday at 7:30pm, before the cloud run, and a **Sync Game Project** shortcut on the Desktop syncs any time (say, mid-week when you change the task). It copies text only: the task file (any file named like task, todo, weekly, roadmap, plan or sprint; or set `TASK_FILE=` in `~/MorningBriefing/game_sync.conf`), Markdown notes, the file tree, GDScript files, scene outlines, recent commits and open issues, into `memory/game_project/` in this repo. Log: `~/MorningBriefing/game_sync.log`.

## Handy commands

- A particular call: `bash ~/MorningBriefing/podcastmemory/engine/mac/record_at_home.sh 2026-11-16 am` (or `pm`, or `eve` on a weekend date; saves to iCloud)
- Quick sample (the first part only): `bash ~/MorningBriefing/podcastmemory/engine/mac/record_at_home.sh 2026-11-16 am quick`
- `record_kokoro.sh` still works and does the same thing.
- Log: `~/MorningBriefing/record.log` (when started from the Desktop)
- Stop a recording: close its Terminal window (or press Ctrl-C).
