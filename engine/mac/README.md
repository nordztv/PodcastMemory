# Recording on the MacBook Pro (Fish Audio S2-Pro)

Set up 25 October 2026 at Scott's request. The cloud run (9:29pm Sunday to Thursday, for the next morning's episode) writes the script and saves it to GitHub. The MacBook Pro then records it in Scott's reference voice with Fish Audio S2-Pro, and saves the audio to iCloud Drive > Morning Briefing.

- There is no schedule: Scott starts each recording by hand (his choice, 25 Oct 2026) by double-clicking **Record Morning Briefing** on the Desktop. In the evening it records the next morning's episode; before noon, that day's. If the script isn't on GitHub yet, it checks every two minutes for up to 4 hours. Leave the Terminal window open (and the Mac plugged in) until it says it's saved.
- It records the full episode with chapter markers (`build_fish.py`) and copies the MP3 plus the answer sheet into iCloud Drive > Morning Briefing, with a notification. (No headlines edition.)
- The voice: `voice.json` holds the defaults (the reference clip `ref_happy1.wav`, "Happy 1", and its transcript `ref_happy.txt`). Put your own settings in `~/MorningBriefing/voice.local.json` instead of editing `voice.json`, so updates never clash. For example `{"ref": "~/Voices/me.wav", "ref_text": "~/Voices/me.txt"}` (a 10 to 30 second WAV and its exact transcript).
- If Fish fails, the episode is recorded with the show's Kokoro voice instead.
- Fish S2-Pro is free for personal, non-commercial use (Fish Audio Research License).

Keep the Mac awake and plugged in while it records (the script stops it sleeping, but closing the lid on battery will pause it).

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

## Kokoro test (compare with Fish)

Added 27 Oct 2026 at Scott's request. Records the episode in the show's Kokoro voice (the one the cloud uses) so you can compare it with Fish. It never touches the Fish recording.

- Full episode: `bash ~/MorningBriefing/podcastmemory/engine/mac/record_kokoro.sh 2026-10-27` -> `Morning_Briefing_2026-10-27_kokoro.mp3`
- Quick sample (opening section only, a few minutes): add `quick`, e.g. `record_kokoro.sh 2026-10-27 quick` -> `..._kokoro_sample.mp3`
- Or copy `Record Morning Briefing (Kokoro test).command` to the Desktop and double-click it.
- The result is copied to iCloud Drive > Morning Briefing and opened when done. It sets up anything missing on its first run. Log: `~/MorningBriefing/record_kokoro.log` (when started from the Desktop file).

## Handy commands

- Record a particular day: `bash ~/MorningBriefing/podcastmemory/engine/mac/record_at_home.sh 2026-10-27` (saves to iCloud), or just rebuild the MP3: `~/MorningBriefing/fish/bin/python ~/MorningBriefing/podcastmemory/engine/mac/build_fish.py 2026-10-27` (lands in `~/podcast/out/`)
- Log: `~/MorningBriefing/record.log`
- Stop a recording: close its Terminal window (or press Ctrl-C). Running it again carries on where it stopped.
