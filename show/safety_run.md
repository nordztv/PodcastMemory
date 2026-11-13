# Safety-net run

Followed by the scheduled task at about 4:50am Sydney time every weekday (Scott's choice, 13 Nov 2026). The evening run should already have delivered this morning's call. This run only acts if it didn't. Work unattended; never ask questions.

Let `DATE` = **today's** Sydney date, `EP` = `REPO/archive/YYYY/MM/DATE`.

1. If `EP/delivered_am.txt` or `EP/delivered.txt` exists (even one that says "script only, not voiced": Scott was told last night): everything is fine. Stop. No message, no notification, no commit.
2. If all six morning scripts exist (`EP/script/01_opening_world.txt` to `06_japan.txt`) but nothing was delivered: the audio failed. Run `sh engine/setup.sh`, then `sh engine/build_episode.sh DATE am`, send `~/podcast/out/Mizuki_DATE_morning_call.mp3` with SendUserFile (status "proactive", display "attach"), create `EP/delivered_am.txt`, commit and push. If the voice engine is blocked, follow `show/daily_run.md` step 6b (send the readable script and say so).
3. If there are no scripts, or only some of the six: the evening run didn't finish. Keep any parts that are complete and write the rest. Follow `show/daily_run.md` from the start, with these limits so it's out **before 6:00am**: a shorter morning call (about 3,000 words: opening and the two biggest world stories, two Australian stories, two tech, two games, the actress and one film story, a short Japan part, the challenge and one question), research limited to twenty minutes, and the memory updates done after delivery. On a Monday this also means her Sunday week update never ran: after delivering, do `show/daily_run.md` step 2b (her week's journal, money, arcs and audit) and say so in the message. At 5:40am deliver whatever is built.
4. In cases 2 and 3, tell Scott in one short SendUserMessage that the evening run didn't deliver and what this run did, and send a push notification saying the morning call is ready (or that it couldn't be recorded).
