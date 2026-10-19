Scheduled run access test: failed
Time (UTC): 2026-10-19T07:43Z
1. Clone repo (sparse, no voice_backup): yes. add_repo not needed. git identity set.
2a. setup.sh: no. Blocked by auto-mode permission classifier ("Code from External"); did not run.
2b. tts.py voice test: no. NO_SUCHFILE: /root/tts/kokoro-v1.0.onnx missing (model not installed because setup.sh was blocked). No MP3, no duration.
3a. current_time tool: no. Tool not present in this session (not found via ToolSearch); used `date -u` instead.
3b. WebSearch "ABC News Australia politics": yes (results returned).
3c. WebFetch abc.net.au/news: yes (HTTP 200, via web-fetch subagent; no direct WebFetch tool in main session).
3d. WebFetch bbc.com/news: no. SITE_BLOCKED: "Access to this website has been blocked".
4. topics.py show: yes (printed header; last daily update 2026-10-19).
5a. SendUserFile: yes (exists).
5b. SendUserMessage: yes (exists).
5c. Chat-history tools ("recent chats"): no (none found).
5d. Claude Docs tools: yes (batch/update/guide/create/read/delete/export/query).
Approvals/blocks: yes. setup.sh command was blocked by the auto-mode classifier. No approval prompts otherwise; BBC blocked at the fetch layer.
