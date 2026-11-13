# Weekend run procedure: the 7pm call

Followed by the scheduled task at about 3:45pm Sydney time every Saturday and Sunday (Scott's choice, 13 Nov 2026). On weekends Mizuki rings Scott **once, at about 7pm**, usually for 10 to 25 minutes. The run happens at about 4pm so the call is ready in time; **in her world it is 7pm** and she has lived the whole day. `show/daily_run.md` has the full detail for every shared step; this file says what's different. Work unattended: never ask questions, make sensible choices, note assumptions in the delivery message.

**Time budget (Sydney):** starts about 3:45pm. Script pushed by about 4:50pm, audio delivered by about 6:15pm. **Hard deadline 6:40pm:** deliver whatever is built (step 6b of `show/afternoon_run.md`, with this run's file names).

Let `DATE` = **today's** Sydney date (a Saturday or Sunday), `REPO` = the clone, `EP` = `REPO/archive/YYYY/MM/DATE`. If `EP/delivered.txt` exists, or today is a weekday: stop, silently.

## 1. Set up and read

`sh REPO/engine/setup.sh` in the background; git identity "Claude", noreply@anthropic.com. Run `python3 REPO/engine/preflight.py DATE`. Read in full `show/bible.md`, `show/host.md`, `show/format_tuning.md`, `show/mizuki/DIGEST.md`, `memory/mizuki.md` (Her weekends: what she told him on Friday she'd do), `memory/mizuki_life.md`, `memory/mizuki_home.md`, `memory/mizuki_timeline.md`, `memory/mizuki_arcs.md`, `memory/people_timelines.md`, `memory/about_scott.md`, `memory/scott_private.md`, `memory/open_threads.md`, `memory/callbacks.md`, `memory/questions.md`, `memory/calls_memory.md`, `memory/recent_calls.md`, `memory/memories_told.md`, `memory/voice_notes.md`, `show/mizuki/CALENDAR.md` (this week: a festival, birthday or anniversary that falls today is marked on this call, bible section 6, Dates), and what she said on the last 5 days of calls (all parts; the calls of 12 and 13 Nov 2026 were made under older rules: avoid repeating their stories, never copy their framing). On Sunday also read Saturday's call, and don't repeat it.

## 2. Her day (it is 7pm for her)

Roll `python3 engine/life_dice.py DATE` and live her whole day up to 7pm (`show/daily_run.md` step 2c: real events first, real prices, the ledger for any fund money, an energy row for DATE in `memory/mizuki_life.md`, a dated line in `memory/mizuki_timeline.md`).
- **Saturday:** her morning (a sleep-in after Friday's film or hitokara), the fish market and her "one good thing", Nana's K-pop dance class, whatever she planned on Friday; by 7pm she's home, cooking or about to go out.
- **Sunday:** her parents' video call in the morning, Fiona's brunch once a month, the gachapon shelf dusted, and by 7pm the okonomiyaki is on the hotplate or just eaten (photo to her mum for a score).
Whether Friday's plans happened is for the dice and the real weather to decide; she tells him honestly. She knows the real world only up to about 4pm (when this is written): the evening's weather is the Bureau's forecast, and she never claims to have seen something real that happened after four.

## 3. What Scott sent

Read his page exactly as in `show/daily_run.md` step 3 and file what isn't filed. Today's `mood`, `day` and `heard` taps, answers to Friday's questions and anything he texted her get a response in this call (set `day: true` in `filed`).

## 4. Research (short: about fifteen minutes)

The weekend's one or two biggest news stories from the allowed sources (bible section 4), only if they matter; the Bureau's forecast for tonight and tomorrow; one thing each from his games and films worlds that happened since Friday (a launch, a result, a release he was waiting on); due open threads (keep promises, re-check facts); and anything real that touches her day (a festival she went to, the film she saw, prices she paid). On Saturday, one idea for his Sunday if the weather changed Friday's suggestions (something for him and his son, or the three of them).

## 5. Write the call

One relaxed evening call from her flat. Before writing, decide in a few lines of notes what's on her mind tonight: her day, how he is (his taps and texts), anything she'd been saving for him, a film or game, the news only if something big happened. Then write it the way she'd say it (bible sections 0, 2, 3 and 5; `show/host.md`, How she actually talks): her own hello ("Konbanwa" fits, or anything else, never the same as last time), wherever her mind goes, and goodnight ("oyasumi"; on Sunday, that she'll ring in the morning). Usually 10 to 25 minutes (about 1,400 to 3,400 words), shorter when she's tired, longer when something good happened. A story told properly, a message from her people or a photo fit well on a weekend evening, but none is required. No challenge unless one of them brings it up. The texture of someone at home on a weekend evening: the hotplate, the possums, the rice cooker.

**Files.** Write the call as plain text files in `EP/script/`, one per stretch of talk, named `eve_01_<subject>.txt`, `eve_02_<subject>.txt` and so on, where `<subject>` is two to four lowercase words joined by hyphens saying what that stretch is about (`eve_01_rough-night-and-the-possums.txt`, `eve_02_the-housing-numbers.txt`). Start a new file wherever the talk moves to something new; usually three to eight files. The names become the chapter titles in his player and never appear in what she says.

Then: `python3 engine/check_script.py DATE eve` (fix every FIX line); write `EP/shownotes.json`, `EP/rating_items.json` and `EP/notes.md`; put the day on his page (`days/DATE`, `set`, as in `show/daily_run.md` step 5, His page: one section per `eve_` file); add promises and dated facts to `memory/open_threads.md`. Commit and push ("Calls DATE: weekend script").

## 6. Build and deliver

`nohup sh REPO/engine/build_episode.sh DATE eve > ~/podcast/build.log 2>&1 &`, poll until it prints a duration. Output: `~/podcast/out/Mizuki_DATE_evening_call.mp3`. SendUserFile (status "proactive", display "attach"), caption: the length and what's in it in one line. Create `EP/delivered.txt` with the time and include it in the memory commit. Fill in the length in `EP/shownotes.json`, run `python3 engine/shownotes.py` and publish it to the URL in `show/shownotes_url.txt`. One short SendUserMessage: what's in the call in two lines, her question written out, anything that failed, and the sources. If the voice engine is blocked or it's 6:40pm, follow `show/afternoon_run.md` step 6b with the file name `EP/Mizuki_DATE_evening_call_script.txt` and the marker `EP/delivered.txt`.

## 7. Update memory, then commit

As `show/daily_run.md` step 8 for what this call touched: a `## DATE (Saturday|Sunday)` entry in `memory/recent_calls.md`; `memory/mizuki.md` (what she did, what she said about herself); `memory/mizuki_timeline.md`; `memory/mizuki_life.md` (energy, any spending through the ledger); `memory/questions.md`; `memory/about_scott.md`; `memory/memories_told.md`, `memory/voice_notes.md`, `memory/callbacks.md`, `memory/movie_log.md`, `memory/deep_dives_covered.md`, `memory/people_timelines.md`, `memory/mizuki_home.md` (anything bought at the market), `memory/calls_memory.md` (the day count goes up by one; on the first weekend call of a month, nothing else: the monthly review belongs to the first weekday morning run). Run `python3 engine/ledger.py check`. Rebuild and publish the timeline page if her day changed it. Commit and push ("Calls DATE: weekend memory"). The Monday morning run at about 3am (`show/daily_run.md` step 2b) does the week's journal, money, arcs and audit, and must count this call's day as already lived.
