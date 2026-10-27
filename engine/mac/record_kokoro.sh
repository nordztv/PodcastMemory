#!/bin/bash
# Kept so the old command still works: the Mac recorder now always uses Kokoro (27 Oct 2026), so this just runs it.
#   bash ~/MorningBriefing/podcastmemory/engine/mac/record_kokoro.sh [YYYY-MM-DD] [quick]
exec bash "$(dirname "$0")/record_at_home.sh" "$@"
