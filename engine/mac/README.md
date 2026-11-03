# Recording on the MacBook Pro (Kokoro voice)

Set up 25 October 2026 at Scott's request; Kokoro only since 27 October 2026 (Scott's choice: Fish Audio removed). The cloud run (about 8:30pm Sunday to Thursday, for the next morning's episode) writes the script and saves it to GitHub. The MacBook Pro then records it in the show's Kokoro voice (the same voice the cloud uses), and saves the audio to iCloud Drive > Morning Briefing.

- There is no schedule (Scott's choice, confirmed 27 Oct 2026): run the one command below in Terminal, or double-click **Record Morning Briefing** on the Desktop. In the evening it records the next morning's episode; before noon, that day's. If the script isn't on GitHub yet, it checks every two minutes for up to 4 hours. Leave the Terminal window open (and the Mac plugged in) until it says it's saved.
- It records the full episode with chapter markers (`engine/build_episode.sh`, the same build the cloud uses) and copies the MP3 plus the answer sheet into iCloud Drive > Morning Briefing, with a notification.
- The voice and its moods are set in `engine/tts.py` (shared with the cloud). The scripts' delivery tags are mapped to Kokoro's six moods automatically, and same-mood sentences are rendered together in paragraph-sized chunks (2 Nov 2026), so a `git pull` gives the Mac the same improvements.
- It keeps the Mac awake while it records, but closing the lid on battery will pause it.

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

It sets up anything missing, waits for the script if it isn't on GitHub yet, records the episode in Kokoro and saves it with the sheet to iCloud Drive > Morning Briefing.

## Weekly game-project sync (3 Nov 2026)

The show's lore, game tech and workshop follow your Game-Prototype weekly task. One-time setup (after the setup above):
```
git -C ~/MorningBriefing/podcastmemory pull -q; bash ~/MorningBriefing/podcastmemory/engine/mac/install_game_sync.sh ~/path/to/Game-Prototype
```
Leave off the path if the folder is in your home, Documents, Developer, Projects, Desktop or GitHub folder (it finds it), or if it's on GitHub as nordztv/Game-Prototype (it clones a copy). It then syncs every Sunday at 7:30pm, before the cloud run, and a **Sync Game Project** shortcut on the Desktop syncs any time (say, mid-week when you change the task). It copies text only: the task file (any file named like task, todo, weekly, roadmap, plan or sprint; or set `TASK_FILE=` in `~/MorningBriefing/game_sync.conf`), Markdown notes, the file tree, GDScript files, scene outlines, recent commits and open issues, into `memory/game_project/` in this repo. Log: `~/MorningBriefing/game_sync.log`.

## Handy commands

- Record a particular day: `bash ~/MorningBriefing/podcastmemory/engine/mac/record_at_home.sh 2026-10-27` (saves to iCloud)
- Quick sample (opening section only): `bash ~/MorningBriefing/podcastmemory/engine/mac/record_at_home.sh 2026-10-27 quick`
- `record_kokoro.sh` still works and does the same thing.
- Log: `~/MorningBriefing/record.log` (when started from the Desktop)
- Stop a recording: close its Terminal window (or press Ctrl-C).
