# Morning Briefing

Scott's personal daily podcast: two phone calls from Mizuki every weekday, one for the walk to work and one for the walk home. A scheduled Claude run makes each episode the evening before (about 8:30pm Sydney time, Sunday to Thursday) and delivers it that night. This repository is the show's long-term home: its rules, its voice engine, its memory and its archive.

## Where things live

| Folder | What's in it | Who edits it |
| --- | --- | --- |
| `show/` | The show bible (the rules), the host sheet, Mizuki's life story (`show/mizuki/`), the nightly procedure (`daily_run.md`), weekly tuning, pronunciations, deep-dive topic pools, and the links to the three pages | Scott, or Claude on request |
| `engine/` | The voice engine and the run's tools (below) | Claude |
| `memory/` | Everything the show remembers: Scott (`about_scott.md`, `questions.md`, `open_threads.md`), Mizuki's ongoing life (timeline, money and ledger, arcs, home, people, opinions), the show itself (recent episodes, ratings, callbacks, topics, storylines) | The nightly run (Scott can edit anything) |
| `archive/` | Every episode's script, notes, show notes and rating items, by date | The nightly run |
| `voice_backup/` | The voice model files, so the voice never depends on outside downloads | Claude |
| `old/` | The first version of the show (18 Oct to 11 Nov 2026) | Nobody |

## The run's tools

- `engine/preflight.py DATE`: the day's brief (special rules for the weekday, where Mizuki is for each call, the dice, threads that are due, variety reminders, word budgets).
- `engine/life_dice.py`: rolls Mizuki's day, week, arcs and month, so her life has real ups and downs.
- `engine/ledger.py`: moves money between her savings funds and proves the funds add up.
- `engine/check_script.py DATE`: catches words the voice would say wrongly, and runs the realism check (joke and laugh counts, repeated reactions, timing slips, banned phrases).
- `engine/topics.py`, `engine/challenges.py`: Scott's topic scores and the daily challenge tally.
- `engine/build_episode.sh DATE`: records the episode with chapter markers; `engine/shownotes.py` and `engine/timeline_page.py` build the two pages.

## Scott's three pages (links in `show/`)

- **Answer page** (`answers_url.txt`): how his day is, the challenge, the week's picks, scores and story taps, the day's questions, Ask Mizuki, names she got wrong, what he built, a note, and the weekly review's proposals. The next run reads it all.
- **Show notes** (`shownotes_url.txt`): links, picks and questions for recent episodes.
- **Mizuki's life** (`timeline_url.txt`): her energy, savings, long story arcs, photos and timeline.

## How memory works over years

- `memory/recent_episodes.md` keeps the last 30 days; the first run of each month condenses the last one into `memory/monthly/`, and the first run of each year writes `memory/yearly/`.
- Mizuki's timeline, ledger, questions and what Scott has told the show are kept forever.
- Every script stays in `archive/`. MP3s aren't stored (too big), but the voice is fixed, so any episode can be re-recorded from its script with `sh engine/build_episode.sh YYYY-MM-DD` (or on Scott's Mac: `engine/mac/README.md`).

## Changing the show

Edit `show/bible.md`, or ask Claude in any chat. The scheduled task only says "read `show/daily_run.md` and follow it", so changes take effect from the next episode. `memory/inbox.md` takes notes for the show from any chat.
