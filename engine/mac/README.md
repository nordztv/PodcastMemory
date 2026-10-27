# Recording on the MacBook Pro (Kokoro voice)

Set up 25 October 2026 at Scott's request; Kokoro only since 27 October 2026 (Scott's choice: Fish Audio removed). The cloud run (about 9:30pm Sunday to Thursday, for the next morning's episode) writes the script and saves it to GitHub. The MacBook Pro then records it in the show's Kokoro voice (the same voice the cloud uses), and saves the audio to iCloud Drive > Morning Briefing.

- There is no schedule: Scott starts each recording by hand (his choice, 25 Oct 2026) by double-clicking **Record Morning Briefing** on the Desktop. In the evening it records the next morning's episode; before noon, that day's. If the script isn't on GitHub yet, it checks every two minutes for up to 4 hours. Leave the Terminal window open (and the Mac plugged in) until it says it's saved.
- It records the full episode with chapter markers (`engine/build_episode.sh`, the same build the cloud uses) and copies the MP3 plus the answer sheet into iCloud Drive > Morning Briefing, with a notification.
- The voice and its moods are set in `engine/tts.py` (shared with the cloud). The scripts' delivery tags are mapped to Kokoro's moods automatically.
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

## Handy commands

- Record a particular day: `bash ~/MorningBriefing/podcastmemory/engine/mac/record_at_home.sh 2026-10-27` (saves to iCloud)
- Quick sample (opening section only): `bash ~/MorningBriefing/podcastmemory/engine/mac/record_at_home.sh 2026-10-27 quick`
- `record_kokoro.sh` still works and does the same thing.
- Log: `~/MorningBriefing/record.log` (when started from the Desktop)
- Stop a recording: close its Terminal window (or press Ctrl-C).
