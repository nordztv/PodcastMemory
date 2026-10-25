#!/bin/bash
# Times Fish S2-Pro on this Mac: records the opening section of the newest episode and estimates a full episode.
# Run:  bash ~/MorningBriefing/podcastmemory/engine/mac/speed_test.sh
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
BASE="$HOME/MorningBriefing"; REPO="$BASE/podcastmemory"
git -C "$REPO" pull -q --rebase --autostash || true
[ -x "$BASE/fish/bin/python" ] || { echo "Run install.sh first."; exit 1; }
D="$(basename "$(ls -d "$REPO"/archive/*/*/*/script | sort | tail -1 | xargs dirname)")"
echo "Mac: $(sysctl -n machdep.cpu.brand_string), $(( $(sysctl -n hw.memsize) / 1073741824 )) GB memory. Testing with $D."
rm -rf "$HOME/podcast/render_fish/$D"
FISH_TEST=1 caffeinate -is "$BASE/fish/bin/python" "$REPO/engine/mac/build_fish.py" "$D"
open "$HOME/podcast/out/Morning_Briefing_$D.mp3"
