# Mizuki's calls

Mizuki Tanaka is a fictional friend of Scott's who lives her own life in Sydney and phones him twice every weekday (at about 8am for his walk to work, and at about 4pm for his walk home) and once on weekend evenings at about 7pm. **It is not a podcast, and she doesn't think it is one**: to her these are phone calls to a friend (`show/bible.md`, section 0). This repository is where her world, her memory and the workings behind the calls are kept. (The repository and a few folders still carry older names such as `PodcastMemory`, `show/` and `build_episode.sh`; those are workshop labels and never part of her world.)

## Four scheduled Claude runs

| Run | When (Sydney) | What it does | Procedure |
| --- | --- | --- | --- |
| Mizuki: morning call | about 3am, Monday to Friday | Lives her night and morning, writes and voices that morning's call (and on Mondays, her week in review) | `show/daily_run.md` |
| Mizuki: afternoon call | about 12:45pm, Monday to Friday | Reads what Scott messaged that morning, checks the day's news, weather and trains, writes and voices the 4pm call | `show/afternoon_run.md` |
| Mizuki: weekend call | about 3:45pm, Saturday and Sunday | Lives her day and prepares the one weekend call, which for her happens at 7pm | `show/weekend_run.md` |
| Mizuki: safety net | about 5:50am, Monday to Friday | Makes the morning call only if the 3am run failed | `show/safety_run.md` |

Each weekday call runs 40 to 50 minutes; the weekend call 10 to 25.

## Where things live

| Folder | What's in it | Who edits it |
| --- | --- | --- |
| `show/` | The rulebook (`bible.md`), who Mizuki is (`host.md`), her life story (`show/mizuki/`), the run procedures, weekly tuning, pronunciations, topic pools, and the links to Scott's three pages | Scott, or Claude on request |
| `engine/` | The voice and the runs' tools (below) | Claude |
| `memory/` | What she knows about Scott (`about_scott.md`, `questions.md`, `open_threads.md`), her ongoing life (timeline, money and ledger, arcs, home, people, opinions), and the story of their calls (recent calls, callbacks, topics) | The runs (Scott can edit anything) |
| `archive/` | What she said on each day's calls, with notes and links, by date | The runs |
| `voice_backup/` | The voice model files, so her voice never depends on outside downloads | Claude |

## The runs' tools

- `engine/preflight.py DATE`: the day's brief (the weekday's habits, where she is for each call, the dice, threads that are due, variety reminders, word budgets).
- `engine/life_dice.py`: rolls her day, week, long stories and month, so her life has real ups and downs.
- `engine/ledger.py`: moves money between her savings funds and proves they add up.
- `engine/audit_mizuki.py`: the Sunday consistency check of her week against her fixed facts.
- `engine/check_script.py DATE [am|pm|eve]`: catches words the voice would say wrongly, anything that breaks the "just a phone call" world, and joke, timing and length problems.
- `engine/topics.py`, `engine/challenges.py`: Scott's interests and the daily challenge tally.
- `engine/build_episode.sh DATE [am|pm|eve]`: voices a call (no music) with chapter markers; `engine/shownotes.py` and `engine/timeline_page.py` build two of the pages.

## Scott's three pages (links in `show/`)

- **Messages to Mizuki** (`answers_url.txt`): to her, these are texts from Scott (how his day is, the challenge, answers to her questions, anything he asks or tells her). A separate "behind the scenes" part is for Claude only and she never sees it: scores, story taps, names she mispronounced, the weekly review.
- **Links from Mizuki** (`shownotes_url.txt`): the things she mentioned on the phone.
- **Mizuki's life** (`timeline_url.txt`): her energy, savings, long stories, photos and timeline.

## Changing things

Edit `show/bible.md`, or ask Claude in any chat. The scheduled runs only say "read the procedure and follow it", so changes take effect from the next call. `memory/inbox.md` takes notes from any chat.
