# Daily run procedure

Followed by the scheduled task every weekday morning (Monday to Friday; no weekend episodes). The run starts about 2:45am Sydney time; the episode MUST be delivered before 6:00am. Work unattended: never ask questions, make sensible choices, and note any assumption in the delivery message. Check the Sydney time with the current_time tool at the start and regularly.

**Time budget (Sydney):** setup and memory read by about 3:05; research and script written and committed by about 4:10; audio rendering starts by 4:15 (about 40 minutes for 80 minutes of audio). If it's past 5:40 and rendering isn't finished, join whatever sections are done and deliver those.

Let `DATE` = today's Sydney date (YYYY-MM-DD), `REPO` = the clone of nordztv/podcastmemory, `EP` = `REPO/archive/YYYY/MM/DATE`.

## 1. Set up (run setup in the background while reading)

- `sh REPO/engine/setup.sh` (installs the voice engine; falls back to this repo's voice_backup/ if the upstream links fail). Test with a one-line text file: `python3 REPO/engine/tts.py test.txt test.mp3`.
- Git identity for commits: name "Claude", email noreply@anthropic.com.

## 2. Read the show and its memory

Read, in full: `show/bible.md`, `memory/actress_of_the_month.md`, `memory/movie_log.md`, `memory/retro_games.md` (the rules, follow them exactly), `memory/topics.md`, `memory/storylines.md`, `memory/questions.md`, `memory/deep_dives_covered.md`, `memory/recent_episodes.md`, and the newest file in `memory/monthly/` (plus the yearly file if one exists). Also check `memory/monthly/` and `memory/yearly/` for an entry from exactly one month or one year ago, for anniversary mentions.

**Rollover:** if `recent_episodes.md` has no entry from the current month yet and this is a new month, do the monthly rollover from bible section 10 now (and the yearly one if it's a new year). Then run `python3 engine/topics.py daily DATE`.

## 3. Scott's answers and recent chats

**Answer sheets:** open the `workout.txt` files from the last 7 days in `archive/` and look under TODAY'S QUESTIONS FROM THE SHOW for any "Your answer:" lines Scott has filled in. For each new answer (not yet marked handled in `memory/questions.md`): record it there, add +10 to that question's topic with `engine/topics.py signal`, and plan the host's reaction plus the single suggestion that goes at the very end of today's episode, just before the goodbye (bible section 6). Only ONE suggestion per episode.

**Inbox:** read `memory/inbox.md`. For each entry under "New": apply it (asked: +10 to the topic, plus follow-ups if noted; liked or wants more: +15; not interested: -20; answer: treat like a sheet answer above; storyline: update `memory/storylines.md`; feedback: adapt today's episode and note it under "Morning Briefing itself" in storylines). Then move the processed entries under "Processed", prefixed with today's date. Use `python3 engine/topics.py signal "Topic" POINTS DATE` for points (bible section 9).

**Chats:** use ToolSearch once to check for tools that read Scott's past Claude conversations (search "recent chats"). They are normally NOT available in scheduled runs; if they are, read his chats since the last episode (at most 3 days; on Mondays, since Friday) and apply them the same way as inbox entries. If not, rely on the inbox and the answer sheets, and don't mention it in the delivery message.

## 4. Research

On Mondays, cover news since Friday's episode. On Fridays, also research the week wrap-up and weekend toddler-friendly Sydney activities (bible section 5, Friday). Follow bible section 4 exactly (strict source rule for news; weather; weekday commute check; main topics first; minor topics checked for anything hot). Mark hot topics with `python3 engine/topics.py hot "Topic" UNTIL` (today plus 3 days).

## 5. Write the script

Write the 11 sections from bible section 5 as plain text files in `EP/script/` (`01_opening_world.txt` ... `11_chat_outro.txt`), following the host, humour, tone, writing and question rules in bible sections 2, 3 and 6. Choose deep dives per bible section 7 (refill a pool if it's running low). Add any new tricky names to `show/pronunciations.json`.

Also write:
- `EP/workout.txt`: today's workout (bible section 8).
- `EP/notes.md`: running order, deep-dive topics, today's questions (with the host's joke answers), topics hot today, and a Sources list (every link used; news links only from the six allowed sources).

Commit and push now (message "Episode DATE: script"), so the work is safe even if rendering fails.

## 6. Build the audio

`nohup sh REPO/engine/build_episode.sh DATE > ~/podcast/build.log 2>&1 &`, then poll with sleep until it prints a duration. While it renders, do step 8. Output: `~/podcast/out/Morning_Briefing_DATE.mp3`.

## 7. Deliver

- SendUserFile (status "proactive", display "attach") with files [the MP3, `EP/workout.txt`], caption: episode length, the three best stories, today's workout focus.
- One short SendUserMessage: running order in a few lines and the deep dives; "Today's questions for you" written out; topic changes (hot topics, promotions to main, drop-offs, new topics); any storyline updates; anything that failed (a site blocked, chat history unavailable, a section skipped); and the Sources list.

## 8. Update memory (while the audio renders), then commit

- `memory/recent_episodes.md`: add today's entry at the top: `## DATE (weekday)`, length (fill in once known), main stories (10 to 15, compact), deep dives, workout focus, questions asked, and a "Follow up" line (upcoming votes, results, releases, developing stories).
- `memory/deep_dives_covered.md`: add today's lore, game tech, effects and director topics, plus workshop and chat topics, at the top of the table.
- `memory/questions.md`: add today's questions (Answer: Not yet, Handled: no); for older ones Scott answered, fill in his answer ("DATE: a few words") and set Handled to the date the episode responded.
- `memory/retro_games.md`: on Mondays add the new pick (status Recommended); on Wednesdays mark the retrospective done. When Scott says (sheet, inbox or chat) whether he played and enjoyed a game, fill in Played, Verdict (Liked, Disliked or Mixed) and a short comment in his words, then pick the next Monday's game with that in mind.
- `memory/actress_of_the_month.md`: on a new month, add the new actress at the top.
- `memory/movie_log.md`: add a row for every film featured or recommended today (Actress of the Month, effects or director deep dive, any specific recommendation), with director, cast, genre and country, and where it was featured. Update the Directors table (new director, or add the film and linked actresses to an existing one). When Scott says (sheet, inbox or chat) he watched a film, fill in Watched, Verdict (Liked, Disliked or Mixed) and his comment.
- `memory/storylines.md`: update any storyline with new developments from Scott's chats (status and last update date); add a new storyline when one of his projects or plans clearly becomes a long-running arc.
- Never log personal or sensitive matters. Respect anything Scott edited by hand.
- Commit and push ("Episode DATE: memory"). If a push is rejected because the remote changed (Scott edited on GitHub), `git pull --rebase` and push again; keep his changes.
