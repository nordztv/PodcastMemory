# Afternoon run procedure: the walk-home call

Followed by the scheduled task at about 1:45pm Sydney time every weekday (Scott's choice, 13 Nov 2026). It makes **today's afternoon call** (parts 07 to 11), the one Mizuki makes at about 4pm from the shop's quiet hour as Scott walks from Hyde Park to Green Square. It exists so that by 4pm she really knows the day: lunchtime's news, the real weather, his train home, and what he tapped or wrote this morning. `show/daily_run.md` (the evening run) made this morning's call and has the full detail for every shared step; this file says what's different. Work unattended: never ask questions, make sensible choices, note assumptions in the delivery message.

**Time budget (Sydney):** starts about 1:45pm. Script pushed by about 2:40pm, audio delivered by about 3:30pm. **Hard deadline 3:50pm:** deliver whatever is built (step 6b). Check the time at the start and regularly (`TZ=Australia/Sydney date`).

Let `DATE` = **today's** Sydney date, `REPO` = the clone, `EP` = `REPO/archive/YYYY/MM/DATE`.

## 0. Should this run happen?

- If `EP/delivered_pm.txt` or `EP/delivered.txt` exists: stop, silently.
- If it's Saturday or Sunday: stop, silently.
- If `EP/script/01_opening_world.txt` doesn't exist (no morning call was made today): still make the afternoon call. Roll her day yourself (`show/daily_run.md` step 2c), and have her say in a line that this morning got away from her.

## 1. Set up

`sh REPO/engine/setup.sh` in the background; git identity "Claude", noreply@anthropic.com. Run `python3 REPO/engine/preflight.py DATE`.

## 2. Read

In full: `show/bible.md`, `show/host.md`, `show/format_tuning.md`, **`EP/day_plan.md`** (her day as the evening run planned it: follow it, add to it, never contradict it), **this morning's scripts** `EP/script/01` to `06` and `EP/notes.md` (what she already told him today: don't repeat a story, do pick up anything she promised to come back to "at four"), `show/mizuki/DIGEST.md`, `memory/mizuki.md`, `memory/mizuki_life.md`, `memory/mizuki_home.md`, `memory/about_scott.md`, `memory/open_threads.md`, `memory/callbacks.md`, `memory/questions.md`, `memory/challenges.md`, `memory/storylines.md`, `memory/deep_dives_covered.md`, `show/topic_pools.md`, `memory/movie_log.md`, `memory/memories_told.md`, `memory/voice_notes.md`, `memory/recent_calls.md`, and the afternoon parts (07 to 11) of the last 5 days of calls. Open anything else `show/daily_run.md` step 2 lists when today's call needs it.

## 3. What Scott sent today

Read the answer page exactly as in `show/daily_run.md` step 3 (answers, filed, the weekly review reply, the inbox) and file whatever isn't filed. The point of this run is **today's** document, `answers/DATE`:
- `mood`, `day`, `heard`: how his day is going. She responds in this call, early, the way a friend would (bible section 6, How's your day). If he tapped that he didn't pick up this morning, she catches him up in a line.
- `challenge`: if he's already tapped Done, she's delighted; if not, she asks, lightly.
- his answer to this morning's question, Ask Mizuki, names, notes: she reacts **today**.
Nothing there means nothing assumed. Never invent what he said.

## 4. Research (short: about fifteen minutes)

- **Since last night:** check the allowed news sources (bible section 4) for anything big since the morning call was written, and for developments in stories she told this morning. One or two items at most, told as "I read this on my break". Nothing new is fine: say nothing.
- **Weather now:** the Bureau's current Sydney observations and this afternoon's and evening's forecast (and the radar or warnings if storms are about). She can now say what it's actually doing.
- **His way home:** Sydney Trains and T8 status now (transportnsw.info); mention only real trouble.
- **Open threads** due today (preflight lists them): keep promises, re-check facts.
- **Deep dives:** choose and research the effects and director topics (bible section 7) and the workshop job.
- **Fridays:** weekend toddler-friendly Sydney activities from real current listings (weather in mind), her own weekend plan at real prices, and the project check-in (`show/daily_run.md` step 4).

## 5. Write the call

Write `07_walkhome.txt`, `08_effects.txt`, `09_director.txt`, `10_workshop.txt`, `11_chat_outro.txt` in `EP/script/` (about 2,150 words; Fridays about 2,450; about 15 per cent shorter when her energy is 4 or less), following bible sections 2, 3, 5 and 6. It's a second call, not a continuation: she rings, says where she is, and has maybe twenty minutes before the evening crowd. Today's lunch rush comes from `EP/day_plan.md`. She asks how the challenge went and owns up about hers, asks one or two questions (never repeating `memory/questions.md`), reacts to his answers, and says goodbye for his evening (Friday: the weekend send-off with her photo of the week, weekend ideas, defending the picks, the project check-in, and "what are you up to next week?"; the weekly review is behind the scenes and she never mentions it).

Then:
- `python3 engine/check_script.py DATE pm`: fix every FIX line, look at every CHECK line.
- Add this call's parts to `EP/shownotes.json`, `EP/rating_items.json` and `EP/notes.md` (keep the morning's entries), and add its sources.
- Answer page: `get` `days/DATE`, then `update` it (pinned with `if_version`) with the full `sections` list (morning parts plus these five) and the full `questions` list (the morning's question first, so its number doesn't change).
- `memory/open_threads.md`: new promises and dated facts from this call; close the ones dealt with.
- Commit and push ("Calls DATE: afternoon script").

## 6. Build and deliver

`nohup sh REPO/engine/build_episode.sh DATE pm > ~/podcast/build_pm.log 2>&1 &`, poll until it prints a duration. Output: `~/podcast/out/Mizuki_DATE_walk_home_call.mp3`. SendUserFile (status "proactive", display "attach"), caption: length and what's in it in one line. Create `EP/delivered_pm.txt` with the time. Fill in the length in `EP/shownotes.json`, run `python3 engine/shownotes.py` and publish it to the URL in `show/shownotes_url.txt` (Artifact tool: `read`, then `publish` with that `url`).

One short SendUserMessage: what's in the call in two or three lines, the questions written out, anything that failed, and the sources. On Fridays add the "Weekly review" section.

## 6b. If the voice engine is blocked, or it's 3:50pm

Try setup once more, then stop trying. Join the five parts into `EP/Mizuki_DATE_walk_home_call_script.txt` (tags removed), commit it, send it with SendUserFile, and say plainly at the top of the message that the walk-home call couldn't be recorded today (his Mac can record it: `engine/mac/README.md`). If rendering is only partly done at 3:50pm, join and send the parts that are finished.

## 7. Friday: weekly review

Do `show/daily_run.md` step 7b here, after the script is pushed or while the audio renders.

## 8. Update memory, then commit

Everything in `show/daily_run.md` step 8 that this call touched: add the afternoon's stories, deep dives, questions and follow-ups to today's entry in `memory/recent_calls.md` (and the day's total length); `memory/deep_dives_covered.md`, `memory/questions.md`, `memory/movie_log.md`, `memory/mizuki.md` (her shift, her challenge, anything new she said), `memory/mizuki_timeline.md`, `memory/about_scott.md` (How he's been, and anything he told her today), `memory/callbacks.md`, `memory/memories_told.md`, `memory/voice_notes.md`, `memory/scott_taught_me.md`, `memory/calls_memory.md` (the count of days goes up once a day, here), on Fridays `memory/photo_log.md` and `memory/weekly_reviews.md`. Run `python3 engine/ledger.py check`. If her timeline, savings, arcs, photos or energy changed, rebuild and publish the timeline page. Commit and push ("Calls DATE: afternoon memory"); on a rejected push, `git pull --rebase` and push again.
