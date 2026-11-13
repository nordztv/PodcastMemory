# Afternoon run procedure: the walk-home call

Followed by the scheduled task at about 12:45pm Sydney time every weekday (Scott's choice, 13 Nov 2026). It makes **today's afternoon call**, the one Mizuki makes at about 4pm from the shop's quiet hour as Scott walks from Hyde Park to Green Square. It exists so that by 4pm she really knows the day: lunchtime's news, the real weather, his train home, and what he tapped or wrote this morning. `show/daily_run.md` (the 3am morning run) made this morning's call and has the full detail for every shared step; this file says what's different. Work unattended: never ask questions, make sensible choices, note assumptions in the delivery message.

**Time budget (Sydney):** starts about 12:45pm. Script pushed by about 2:15pm, audio delivered by about 3:15pm. **Hard deadline 3:50pm:** deliver whatever is built (step 6b). Check the time at the start and regularly (`TZ=Australia/Sydney date`).

Let `DATE` = **today's** Sydney date, `REPO` = the clone, `EP` = `REPO/archive/YYYY/MM/DATE`.

## 0. Should this run happen?

- If `EP/delivered_pm.txt` or `EP/delivered.txt` exists: stop, silently.
- If it's Saturday or Sunday: stop, silently (weekends have their own run).
- If there are no `EP/script/am_*` files (no morning call was made today): still make the afternoon call. On a Monday, if `memory/mizuki_life.md` has no "Week ending" entry for yesterday, do `show/daily_run.md` step 2b first. Roll her day yourself (`show/daily_run.md` step 2c), and have her say in a line that this morning got away from her.

## 1. Set up

`sh REPO/engine/setup.sh` in the background; git identity "Claude", noreply@anthropic.com. Run `python3 REPO/engine/preflight.py DATE`.

## 2. Read

In full: `show/bible.md`, `show/host.md`, `show/format_tuning.md`, **`EP/day_plan.md`** (her day as the morning run planned it: follow it, add to it, never contradict it), **this morning's call** `EP/script/am_*` and `EP/notes.md` (what she already told him today: don't repeat a story, do pick up anything she promised to come back to "at four"), `show/mizuki/DIGEST.md`, `memory/mizuki.md`, `memory/mizuki_life.md`, `memory/mizuki_home.md`, `memory/now_playing.md`, `memory/ffxiv.md`, `memory/about_scott.md`, `memory/scott_private.md`, `memory/open_threads.md`, `memory/callbacks.md`, `memory/questions.md`, `memory/challenges.md`, `memory/storylines.md`, `memory/deep_dives_covered.md`, `show/topic_pools.md`, `memory/movie_log.md`, `memory/memories_told.md`, `memory/voice_notes.md`, `memory/calls_memory.md`, `memory/recent_calls.md`, and the afternoon calls (`pm_*`, or `07` to `11` before 16 Nov) of the last 5 days, plus any weekend calls among them (the calls of 12 and 13 Nov 2026 were made under older rules: avoid repeating their stories, never copy their framing). Open anything else `show/daily_run.md` step 2 lists when today's call needs it.

## 3. What Scott sent today

Read the answer page exactly as in `show/daily_run.md` step 3 (answers, filed, the weekly review reply, the inbox) and file whatever isn't filed. The point of this run is **today's** document, `answers/DATE`:
- `mood`, `day`, `heard`: how his day is going. She responds in this call, early, the way a friend would (bible section 6, How's your day), and this run sets `day: true` in `filed` so tomorrow morning's call doesn't answer it again. If he tapped that he didn't pick up this morning, she catches him up in a line.
- `challenge`: if he's already tapped Done, she's delighted; if not, she asks, lightly.
- his answer to this morning's question, Ask Mizuki, names, notes: she reacts **today**.
Nothing there means nothing assumed. Never invent what he said.

## 4. Research (short: about fifteen minutes)

- **Since last night:** check the allowed news sources (bible section 4) for anything big since the morning call was written, and for developments in stories she told this morning. One or two items at most, told as "I read this on my break". Nothing new is fine: say nothing.
- **Weather now:** the Bureau's current Sydney observations and this afternoon's and evening's forecast (and the radar or warnings if storms are about). She can now say what it's actually doing.
- **His way home:** Sydney Trains and T8 status now (transportnsw.info); mention only real trouble.
- **Open threads** due today (preflight lists them): keep promises, re-check facts.
- **Anything she wants to get into:** if something today prompted a story or a how-it-was-made (bible section 5, Stories), research it properly.
- **Fridays:** what's really on in Sydney this weekend that he might like (toddler-friendly, weather in mind), her own weekend plan at real prices, and anything new on a project of his he's mentioned lately.

## 5. Write the call

It's a second call, not a continuation: she rings from the shop's quiet hour, says where she is, and has a long quiet stretch before the evening crowd (Mr Kondo lets her take it). Before writing, decide in a few lines of notes what's on her mind now: how today's shift went (from `EP/day_plan.md`), how he is (what he tapped or texted today), anything she left for four o'clock this morning (in `EP/day_plan.md`; she picks it up, or doesn't get to it and says so), anything big in the news since last night, and what she's doing tonight. Then write it the way she'd say it (bible sections 0, 2, 3 and 5; `show/host.md`, How she actually talks), with her own hello (different from this morning's) and a goodbye when he's nearly home or someone needs her. 40 to 50 minutes (about 5,400 to 6,700 words; Scott's choice, 13 Nov 2026): nearer 40 when she's tired, nearer 50 when she's bright. It's long, so let it breathe: the shift told properly, a story, his family, a real back-and-forth about what he sent her, a rant about the news. Don't repeat what she said this morning (`EP/script/am_*`).
- Her game (`memory/now_playing.md`): if she didn't bring it up this morning and it's been a couple of days, this is a good moment (run `python3 engine/games.py mentioned DATE` if she does). Tonight's plans can include it, or a raid night (`memory/ffxiv.md`).
- Things that may come up, none required: the challenge if one was set (how he went, and honestly how she went), a question if she's curious, a story or how-something-was-made if something prompted it, her photo, a message from her people. `EP/day_plan.md` says what the morning call already used.
- **Friday:** this call usually drifts into weekend talk (her plans at real prices, what he's up to, maybe an idea or two for his weekend from real current Sydney listings, weather in mind, "check before you go"; maybe his game or a project if he's mentioned it lately), and ends with "I'll ring you tomorrow evening". The weekly review is behind the scenes and she never mentions it.
- **The first weekday of a month:** she might ask how he's going in a bigger way, or notice he's gone quiet on something.

**Files.** Write the call as plain text files in `EP/script/`, one per stretch of talk, named `pm_01_<subject>.txt`, `pm_02_<subject>.txt` and so on, where `<subject>` is two to four lowercase words joined by hyphens saying what that stretch is about (`pm_01_rough-night-and-the-possums.txt`, `pm_02_the-housing-numbers.txt`). Start a new file wherever the talk moves to something new; usually three to eight files. The names become the chapter titles in his player and never appear in what she says.

Then:
- `python3 engine/check_script.py DATE pm`: fix every FIX line, look at every CHECK line.
- Add this call's parts to `EP/shownotes.json`, `EP/rating_items.json` and `EP/notes.md` (keep the morning's entries), and add its sources.
- His page: `get` `days/DATE`, then `update` it (pinned with `if_version`) with the full `sections` list (the morning's sections, then one per `pm_` file, as in `show/daily_run.md` step 5, His page) and the full `questions` list (the morning's first, so their numbers don't change), and `challenge` if she set one now.
- `memory/open_threads.md`: new promises and dated facts from this call; close the ones dealt with.
- Commit and push ("Calls DATE: afternoon script").

## 6. Build and deliver

`nohup sh REPO/engine/build_episode.sh DATE pm > ~/podcast/build_pm.log 2>&1 &`, poll until it prints a duration. Output: `~/podcast/out/Mizuki_DATE_walk_home_call.mp3`. SendUserFile (status "proactive", display "attach"), caption: length and what's in it in one line. Create `EP/delivered_pm.txt` with the time and include it in the memory commit (the next run starts from a fresh copy and looks for it). Fill in the length in `EP/shownotes.json`, run `python3 engine/shownotes.py` and publish it to the URL in `show/shownotes_url.txt` (Artifact tool: `read`, then `publish` with that `url`).

One short SendUserMessage: what's in the call in two or three lines, the questions written out, anything that failed, and the sources. On Fridays add the "Weekly review" section.

## 6b. If the voice engine is blocked, or it's 3:50pm

Try setup once more, then stop trying. Join the `pm_` parts into `EP/Mizuki_DATE_walk_home_call_script.txt` (tags removed), commit it, send it with SendUserFile, and say plainly at the top of the message that the walk-home call couldn't be recorded today (his Mac can record it: `engine/mac/README.md`). If rendering is only partly done at 3:50pm, join and send the parts that are finished. Either way create `EP/delivered_pm.txt` (the time, and "script only, not voiced" if no audio went out) and commit it, so tomorrow's morning call knows she rang.

## 7. Friday: weekly review

Do `show/daily_run.md` step 7b here, after the script is pushed or while the audio renders.

## 8. Update memory, then commit

Everything in `show/daily_run.md` step 8 that this call touched: add the afternoon's stories, deep dives, questions and follow-ups to today's entry in `memory/recent_calls.md` (and the day's total length); `memory/deep_dives_covered.md`, `memory/questions.md`, `memory/movie_log.md`, `memory/mizuki.md` (her shift, her challenge, anything new she said), `memory/mizuki_timeline.md` (today's shift, now that she has told it), `memory/about_scott.md` (How he's been, and anything he told her today), `memory/callbacks.md`, `memory/memories_told.md`, `memory/voice_notes.md`, `memory/scott_taught_me.md`, `memory/calls_memory.md` (the count of days goes up once a day, here), on Fridays `memory/photo_log.md` and `memory/weekly_reviews.md`. Run `python3 engine/ledger.py check`. If her timeline, savings, arcs, photos or energy changed, rebuild and publish the timeline page. Commit and push ("Calls DATE: afternoon memory"); on a rejected push, `git pull --rebase` and push again.
