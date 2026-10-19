#!/bin/bash
# Times VoxCPM2 on this Mac: records just the opening section of Tuesday 20 Oct's episode and estimates a full episode.
# Run:  bash ~/MorningBriefing/podcastmemory/engine/mac/speed_test.sh
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
BASE="$HOME/MorningBriefing"; REPO="$BASE/podcastmemory"
git -C "$REPO" pull -q || true
[ -x "$BASE/mlx/bin/mlx_audio.tts.generate" ] || { echo "Run install.sh (or voice_audition.sh) first."; exit 1; }
echo "Mac: $(sysctl -n machdep.cpu.brand_string), $(( $(sysctl -n hw.memsize) / 1073741824 )) GB memory"
rm -rf "$HOME/podcast/render_vox/2026-10-20"
caffeinate -is VOX_TEST=1 python3 "$REPO/engine/mac/build_voxcpm.py" 2026-10-20
open "$HOME/podcast/out/Morning_Briefing_2026-10-20.mp3"
