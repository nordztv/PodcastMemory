#!/bin/bash
# Weekly game-project sync (Scott's choice, 3 Nov 2026): copies the current state of his Godot project
# (Game-Prototype) into this repo's memory/game_project/ folder and pushes it, so the cloud run can build the
# week's episodes around his weekly task. Runs automatically every Sunday at 7:30pm (before the 8:30pm cloud run)
# once install_game_sync.sh has been run; also safe to run by hand any time:
#   bash ~/MorningBriefing/podcastmemory/engine/mac/sync_game_project.sh
# Settings live in ~/MorningBriefing/game_sync.conf (GAME_DIR=..., optional TASK_FILE=...).
# It copies text only: the weekly task file, Markdown notes, the project's file tree, GDScript files (up to a size
# limit), recent commits and open GitHub issues. Art, audio and builds are never copied.
set -e
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
BASE="$HOME/MorningBriefing"; REPO="$BASE/podcastmemory"; CONF="$BASE/game_sync.conf"
OUTDIR="$REPO/memory/game_project"; SNAP="$OUTDIR/snapshot"
notify() { osascript -e "display notification \"$1\" with title \"Morning Briefing\"" >/dev/null 2>&1 || true; }
[ -f "$CONF" ] && . "$CONF"

# Find the project if it isn't configured yet.
if [ -z "$GAME_DIR" ] || [ ! -d "$GAME_DIR" ]; then
  for d in "$HOME"/Game-Prototype "$HOME"/game-prototype "$HOME"/Documents/Game-Prototype "$HOME"/Documents/game-prototype \
           "$HOME"/Developer/Game-Prototype "$HOME"/Projects/Game-Prototype "$HOME"/Desktop/Game-Prototype \
           "$HOME"/Documents/GitHub/Game-Prototype "$HOME"/GitHub/Game-Prototype; do
    [ -f "$d/project.godot" ] && GAME_DIR="$d" && break
  done
fi
if [ -z "$GAME_DIR" ]; then
  GAME_DIR="$(find "$HOME" -maxdepth 4 -type f -name project.godot -path '*[Gg]ame[-_][Pp]rototype*' \
               -not -path '*/Library/*' -not -path '*/.Trash/*' 2>/dev/null | head -1 | xargs -I{} dirname "{}")"
fi
if [ -z "$GAME_DIR" ] && command -v gh >/dev/null && gh repo view nordztv/Game-Prototype >/dev/null 2>&1; then
  GAME_DIR="$BASE/game-prototype"
  [ -d "$GAME_DIR/.git" ] || gh repo clone nordztv/Game-Prototype "$GAME_DIR" -- -q
fi
if [ -z "$GAME_DIR" ] || [ ! -d "$GAME_DIR" ]; then
  echo "Couldn't find your Game-Prototype folder. Put its path in $CONF, for example:"
  echo "  GAME_DIR=\"$HOME/Documents/Game-Prototype\""
  notify "Game sync: couldn't find the Game-Prototype folder"; exit 1
fi
grep -q '^GAME_DIR=' "$CONF" 2>/dev/null || echo "GAME_DIR=\"$GAME_DIR\"" >> "$CONF"
# A clone made by this script is kept up to date; Scott's own working folder is never pulled or changed.
[ "$GAME_DIR" = "$BASE/game-prototype" ] && git -C "$GAME_DIR" pull -q --rebase --autostash || true

git -C "$REPO" pull -q --rebase --autostash || true
rm -rf "$SNAP"; mkdir -p "$SNAP/notes" "$SNAP/scripts"
cd "$GAME_DIR"

# 1. The weekly task: TASK_FILE if set, otherwise any task/todo/weekly/roadmap/plan/sprint file (Markdown or text).
: > "$SNAP/weekly_task.md"
if [ -n "$TASK_FILE" ] && [ -f "$TASK_FILE" ]; then TASKS="$TASK_FILE"
else TASKS="$(find . -maxdepth 3 -type f \( -iname '*.md' -o -iname '*.txt' \) -not -path './.godot/*' -not -path './addons/*' \
          | grep -iE 'task|todo|weekly|week|roadmap|plan|sprint|backlog|milestone' | head -10)"; fi
OLDIFS="$IFS"; IFS=$'\n'
for f in $TASKS; do
  printf '\n\n===== %s (modified %s) =====\n\n' "$f" "$(date -r "$f" '+%Y-%m-%d %H:%M')" >> "$SNAP/weekly_task.md"
  head -c 40000 "$f" >> "$SNAP/weekly_task.md"
done
IFS="$OLDIFS"

# 2. Other notes (README, design docs): Markdown and text files, 40 KB each at most.
find . -maxdepth 3 -type f \( -iname '*.md' -o -iname '*.txt' \) -not -path './.godot/*' -not -path './addons/*' | while read -r f; do
  n="$(echo "${f#./}" | tr '/' '_')"; head -c 40000 "$f" > "$SNAP/notes/$n"
done

# 3. The project's shape: project settings and a file tree (names only, no art or audio content).
[ -f project.godot ] && head -c 20000 project.godot > "$SNAP/project.godot.txt"
find . -not -path './.godot*' -not -path './.git/*' -not -path './addons/*' -not -name '*.import' -not -name '*.uid' \
  | sed 's|^\./||' | sort | head -2000 > "$SNAP/file_tree.txt"

# 4. GDScript files and scene outlines, up to about 400 KB in total, so the show can teach from his actual code.
TOTAL=0
find . -type f \( -name '*.gd' -o -name '*.tscn' \) -not -path './.godot/*' -not -path './addons/*' | sort | while read -r f; do
  s=$(wc -c < "$f"); [ $((TOTAL + s)) -gt 400000 ] && continue; TOTAL=$((TOTAL + s))
  n="$(echo "${f#./}" | tr '/' '_')"
  if [ "${f##*.}" = "tscn" ]; then grep -E '^\[(node|ext_resource|sub_resource)' "$f" | head -300 > "$SNAP/scripts/$n.outline.txt"
  else cp "$f" "$SNAP/scripts/$n"; fi
done

# 5. Recent work: commits from the last 14 days, and open GitHub issues if the project is on GitHub.
if git rev-parse --git-dir >/dev/null 2>&1; then
  git log --since='14 days ago' --date=short --pretty='%ad %s' --stat=100 | head -400 > "$SNAP/recent_commits.txt"
  git status --short | head -200 > "$SNAP/uncommitted.txt"
  if command -v gh >/dev/null; then gh issue list --state open --limit 50 2>/dev/null > "$SNAP/open_issues.txt" || true; fi
fi

cat > "$OUTDIR/snapshot_info.md" <<EOF
# Game project snapshot

- Synced: $(TZ=Australia/Sydney date '+%Y-%m-%d %H:%M %Z') from the Mac (engine/mac/sync_game_project.sh)
- Project folder: $(basename "$GAME_DIR")
- Weekly task file(s): $(echo $TASKS | tr '\n' ' ')
EOF

cd "$REPO"
git add memory/game_project
if git diff --cached --quiet; then echo "Nothing changed since the last sync."; notify "Game sync: nothing new this week"; exit 0; fi
git commit -qm "Game project snapshot $(TZ=Australia/Sydney date +%F)"
git push -q || { git pull -q --rebase && git push -q; }
echo "Synced $(basename "$GAME_DIR") to PodcastMemory."
notify "Game project synced for this week's episodes"
