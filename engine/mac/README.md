# Mac recording (retired)

Retired on 20 October 2026 at Scott's request: episodes are recorded in the cloud only, and arrive in the Claude app.

The two files left here only switch off the Mac's old 3:30am schedule the next time it fires. To tidy up the Mac fully, run in Terminal:

```
launchctl unload ~/Library/LaunchAgents/com.scott.morningbriefing.plist; rm -f ~/Library/LaunchAgents/com.scott.morningbriefing.plist
sudo pmset repeat cancel
rm -rf ~/MorningBriefing ~/podcast
```

The last line deletes the Mac's copy of this repository, the voice models and old renders (episodes already in iCloud Drive > Morning Briefing are kept). The old Mac scripts are in this repository's history.
