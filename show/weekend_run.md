# Weekend run procedure: the 7pm call

Followed by the scheduled task at about 3:45pm Sydney time every Saturday and Sunday (Scott's choice, 13 Nov 2026). On weekends Mizuki rings Scott **once, at about 7pm**, for about half as long as a weekday (about 3,000 words, 20 to 25 minutes). The run happens at about 4pm so the call is ready in time; **in her world it is 7pm** and she has lived the whole day. `show/daily_run.md` has the full detail for every shared step; this file says what's different. Work unattended: never ask questions, make sensible choices, note assumptions in the delivery message.

**Time budget (Sydney):** starts about 3:45pm. Script pushed by about 4:50pm, audio delivered by about 6:15pm. **Hard deadline 6:40pm:** deliver whatever is built (step 6b of `show/afternoon_run.md`, with this run's file names).

Let `DATE` = **today's** Sydney date (a Saturday or Sunday), `REPO` = the clone, `EP` = `REPO/archive/YYYY/MM/DATE`. If `EP/delivered.txt` exists, or today is a weekday: stop, silently.

## 1. Set up and read

`sh REPO/engine/setup.sh` in the background; git identity "Claude", noreply@anthropic.com. Run `python3 REPO/engine/preflight.py DATE`. Read in full `show/bible.md`, `show/host.md`, `show/format_tuning.md`, `show/mizuki/DIGEST.md`, `memory/mizuki.md` (Her weekends: what she told him on Friday she'd do), `memory/mizuki_life.md`, `memory/mizuki_home.md`, `memory/mizuki_arcs.md`, `memory/people_timelines.md`, `memory/about_scott.md`, `memory/open_threads.md`, `memory/callbacks.md`, `memory/questions.md`, `memory/calls_memory.md`, `memory/recent_calls.md`, `memory/memories_told.md`, `memory/voice_notes.md`, `show/mizuki/CALENDAR.md` (this week: a festival, birthday or anniversary that falls today is marked on this call, bible section 6, Dates), and what she said on the last 5 days of calls (all parts; the calls of 12 and 13 Nov 2026 were made under older rules: avoid repeating their stories, never copy their framing). On Sunday also read Saturday's call, and don't repeat it.

## 2. Her day (it is 7pm for her)

Roll `python3 engine/life_dice.py DATE` and live her whole day up to 7pm (`show/daily_run.md` step 2c: real events first, real prices, the ledger for any fund money, an energy row for DATE in `memory/mizuki_life.md`, a dated line in `memory/mizuki_timeline.md`).
- **Saturday:** her morning (a sleep-in after Friday's film or hitokara), the fish market and her "one good thing", Nana's K-pop dance class, whatever she planned on Friday; by 7pm she's home, cooking or about to go out.
- **Sunday:** her parents' video call in the morning, Fiona's brunch once a month, the gachapon shelf dusted, and by 7pm the okonomiyaki is on the hotplate or just eaten (photo to her mum for a score).
Whether Friday's plans happened is for the dice and the real weather to decide; she tells him honestly. She knows the real world only up to about 4pm (when this is written): the evening's weather is the Bureau's forecast, and she never claims to have seen something real that happened after four.

## 3. What Scott sent

Read his page exactly as in `show/daily_run.md` step 3 and file what isn't filed. Today's `mood`, `day` and `heard` taps, answers to Friday's questions and anything he texted her get a response in this call (set `day: true` in `filed`).

## 4. Research (short: about fifteen minutes)

The weekend's one or two biggest news stories from the allowed sources (bible section 4), only if they matter; the Bureau's forecast for tonight and tomorrow; one thing each from his games and films worlds that happened since Friday (a launch, a result, a release he was waiting on); due open threads (keep promises, re-check facts); and anything real that touches her day (a festival she went to, the film she saw, prices she paid). On Saturday, one idea for his Sunday if the weather changed Friday's suggestions (put neutrally, "something for tomorrow"; his family is only mentioned in Friday's weekend ideas).

## 5. Write the call

One relaxed evening call, about 3,000 words (about 15 per cent shorter when her energy is 4 or less), as five plain text files in `EP/script/`:
1. `01_evening_hello.txt` (about 500): must begin exactly "Konbanwa, Scott." Where she is at 7pm, how he is (his taps), and the best thing about her day so far.
2. `02_evening_world.txt` (about 600): what she read today that he'd want to know. Short. No news at all is fine on a quiet day; then this part is more of her day.
3. `03_evening_fun.txt` (about 800): games and films, the way they come up between friends on a weekend: what she watched or played, what he might, anything he was waiting on.
4. `04_evening_story.txt` (about 600): one story told properly: a memory (check `memory/memories_told.md`), something from Japan, a yokai, how a film did something, or a long voice note from one of her people. Her choice, by mood.
5. `05_evening_goodbye.txt` (about 500): her reaction to his answers, one question for him (never one in `memory/questions.md`), what she's doing tonight and tomorrow, and goodnight ("oyasumi"). On Sunday: a line about the week ahead, and that she'll ring in the morning.
No daily challenge on weekends. Bible sections 0, 2, 3 and 6 all apply: it's a phone call from a friend, with fewer jokes than a weekday (about 4 to 6), a whispered secret if one fits, and the texture of someone at home on a weekend evening (the hotplate, the possums, the rice cooker).

Then: `python3 engine/check_script.py DATE eve` (fix every FIX line); write `EP/shownotes.json`, `EP/rating_items.json` and `EP/notes.md`; put the day on his page (`days/DATE`, as in `show/daily_run.md` step 5: `challenge: ""`, `rateLine: ""`, the five sections with keys "evening-hello", "evening-world", "evening-fun", "evening-story", "evening-goodbye", the one question, and the week's picks); add promises and dated facts to `memory/open_threads.md`. Commit and push ("Calls DATE: weekend script").

## 6. Build and deliver

`nohup sh REPO/engine/build_episode.sh DATE eve > ~/podcast/build.log 2>&1 &`, poll until it prints a duration. Output: `~/podcast/out/Mizuki_DATE_evening_call.mp3`. SendUserFile (status "proactive", display "attach"), caption: the length and what's in it in one line. Create `EP/delivered.txt` with the time and include it in the memory commit. Fill in the length in `EP/shownotes.json`, run `python3 engine/shownotes.py` and publish it to the URL in `show/shownotes_url.txt`. One short SendUserMessage: what's in the call in two lines, her question written out, anything that failed, and the sources. If the voice engine is blocked or it's 6:40pm, follow `show/afternoon_run.md` step 6b with the file name `EP/Mizuki_DATE_evening_call_script.txt` and the marker `EP/delivered.txt`.

## 7. Update memory, then commit

As `show/daily_run.md` step 8 for what this call touched: a `## DATE (Saturday|Sunday)` entry in `memory/recent_calls.md`; `memory/mizuki.md` (what she did, what she said about herself); `memory/mizuki_timeline.md`; `memory/mizuki_life.md` (energy, any spending through the ledger); `memory/questions.md`; `memory/about_scott.md`; `memory/memories_told.md`, `memory/voice_notes.md`, `memory/callbacks.md`, `memory/movie_log.md`, `memory/deep_dives_covered.md`, `memory/people_timelines.md`, `memory/mizuki_home.md` (anything bought at the market), `memory/calls_memory.md` (the day count goes up by one; on the first weekend call of a month, nothing else: the monthly review belongs to the first weekday evening run). Run `python3 engine/ledger.py check`. Rebuild and publish the timeline page if her day changed it. Commit and push ("Calls DATE: weekend memory"). The Sunday evening run (`show/daily_run.md` step 2b) does the week's journal, money, arcs and audit a few hours later, and must count this call's day as already lived.
