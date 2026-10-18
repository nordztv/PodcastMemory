# Morning Briefing

Scott's personal daily podcast. A scheduled Claude run builds a new episode every morning at 2:45am Sydney time and delivers it before 6am. This repository is the show's long-term home: its rules, its voice engine, its memory and its archive.

## Where things live

| Folder | What's in it | Who edits it |
| --- | --- | --- |
| `show/` | The show bible (host personality, segments, news sources, rules), pronunciations, deep-dive topic pools | Scott or Claude, on request |
| `engine/` | Voice engine setup, text-to-speech, episode builder, topic scoring tool | Claude |
| `memory/` | What the show remembers: topic scores, storylines, questions, deep dives covered, recent episodes, monthly and yearly summaries | The daily run (Scott can edit anytime) |
| `archive/` | Every episode's script, workout and notes, by date | The daily run |
| Releases | `ep-YYYY-MM-DD`: each episode's MP3. `voice-engine-v1`: backup copy of the voice model files | The daily run |

## How memory works over years

- **Recent:** `memory/recent_episodes.md` keeps the last 30 days in detail.
- **Monthly:** on the first run of each month, last month is condensed into `memory/monthly/YYYY-MM.md`.
- **Yearly:** on the first run of each year, last year is condensed into `memory/yearly/YYYY.md`.
- **Always on:** `memory/storylines.md` (Scott's long-running arcs) and `memory/topics.md` (scored interests) carry across everything.
- Full detail is never lost: every script stays in `archive/`.

## Changing the show

Edit `show/bible.md` (or ask Claude in any chat to change it). The scheduled task only says "read the bible and follow it", so changes take effect the next morning.
