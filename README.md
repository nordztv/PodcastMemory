# Morning Briefing

Scott's personal daily podcast. A scheduled Claude run builds a new episode every weekday morning (Monday to Friday, starting 1:45am) at 1:45am Sydney time and delivers it before 6am. This repository is the show's long-term home: its rules, its voice engine, its memory and its archive.

## Where things live

| Folder | What's in it | Who edits it |
| --- | --- | --- |
| `show/` | The show bible (host personality, segments, news sources, rules), pronunciations, deep-dive topic pools | Scott or Claude, on request |
| `engine/` | Voice engine setup, text-to-speech, episode builder, topic scoring tool | Claude |
| `memory/` | What the show remembers: topic scores, storylines, questions, deep dives covered, recent episodes, monthly and yearly summaries | The daily run (Scott can edit anytime) |
| `archive/` | Every episode's script, answer sheet and notes, by date | The daily run |
| `voice_backup/` | Backup copy of the voice model files (split into parts), used if the original download links ever disappear | Claude |

## How memory works over years

- **Recent:** `memory/recent_episodes.md` keeps the last 30 days in detail.
- **Monthly:** on the first run of each month, last month is condensed into `memory/monthly/YYYY-MM.md`.
- **Yearly:** on the first run of each year, last year becomes a three-page "story so far" in `memory/yearly/YYYY.md`.
- **Always on:** `memory/storylines.md` (Scott's long-running arcs) and `memory/topics.md` (scored interests) carry across everything.
- Full detail is never lost: every script stays in `archive/`. MP3s aren't stored here (too big for a repository), but the voice is fixed, so any episode can be re-recorded identically from its script with `sh engine/build_episode.sh YYYY-MM-DD`.

## Each episode

- **Full episode** (about 75 to 85 minutes), with chapter markers so you can jump between segments.
- **Five-minute headlines edition** for busy mornings.
- **Daily challenge** (like 30 push-ups or a 5 km walk) with your completion rate, tallied in `memory/challenges.md`.
- **Answer sheet** with the challenge's "Done" line, the day's questions and a quick rating.
- **Show notes page**: links, picks and questions for the last 15 episodes, one page updated each morning (link in `show/shownotes_url.txt`).

## Changing the show

Edit `show/bible.md` (or ask Claude in any chat to change it). The scheduled task only says "read the bible and follow it", so changes take effect the next morning.

## Telling the show things

`memory/inbox.md` is how the show hears from you between episodes: things you asked about, liked or didn't, answers, project updates, feedback. In any Claude chat, say something like "add that to my podcast" (the podcast note skill files it), or add a line to the inbox yourself on GitHub. The daily run reads it each morning.

## Answering the host's questions

Each day's `archive/YYYY/MM/DATE/sheet.txt` (`workout.txt` before 21 October 2026) has the host's questions and blank "Your answer:" lines. Fill them in right here on GitHub (the GitHub app works on your phone), or mention your answer in any chat with Claude. The next episode reacts and gives you a suggestion based on what you said.
