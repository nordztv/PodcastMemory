"""Mizuki's own gaming: the retro game she's playing through, and Final Fantasy XIV (Scott's request, 13 Nov 2026).

Usage:
  python3 engine/games.py roll DATE        # what she played on the evening before DATE's call (or DATE's own day on a
                                           # weekend), and whether she brings the game up on DATE's call
  python3 engine/games.py log DATE HOURS "where she got to"   # add a play session to memory/now_playing.md
  python3 engine/games.py mentioned DATE   # she talked about it on DATE's call (resets the "every couple of days" clock)
  python3 engine/games.py status           # the game, hours played of the total, last session, last mention
  python3 engine/games.py finish DATE      # she finished it: moves memory/now_playing.md into memory/games_finished/
                                           # and leaves a fresh template for the next game

The retro game moves only as fast as her evenings allow: about an hour on the evenings she plays it, so a 30-hour game
takes her weeks. Tuesday and Thursday are FFXIV raid nights (memory/ffxiv.md). Seeded by the date, so re-running gives
the same answer. The run turns a session into where she really got to in the real game (look it up: a walkthrough or
wiki, paced by hours played), never invented story.
"""
import datetime as dt, os, random, re, shutil, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOW = f"{REPO}/memory/now_playing.md"
DONE = f"{REPO}/memory/games_finished"
# Chance she plays the retro game on each evening (Monday = 0), from her week in show/mizuki/DIGEST.md.
PLAY = {0: 0.55, 1: 0.10, 2: 0.75, 3: 0.10, 4: 0.40, 5: 0.55, 6: 0.60}
FFXIV = {0: "roulettes or FC-house decorating", 1: "raid night with Tsukimi Noodles (9pm)", 2: "maybe a little FFXIV after the drama",
         3: "raid night with Tsukimi Noodles (9pm)", 4: "", 5: "", 6: ""}
TEMPLATE = """# Now playing

The retro game Mizuki is playing through right now, a session at a time (Scott's request, 13 Nov 2026; `engine/games.py`). Always a pixel-art retro game, or any Final Fantasy. She plays it on what she owns (the Super Famicom Mini, the PS5, later a Switch 2), about an hour on the evenings she plays it, so a long game takes weeks. She brings it up every couple of days as a conversation starter: where she's up to, the story and lore so far, what she loves or hates, a character she's annoyed with. She only knows the game up to where she is; no spoilers past it (and none at all if Scott says he wants to play it). When she finishes, `python3 engine/games.py finish DATE` moves this file into `memory/games_finished/` and the next game starts here.

**Game:** (none yet)
**Platform:** 
**Why she picked it:** 
**Length:** about 0 hours (main story; look it up, e.g. HowLongToBeat)
**Hours played:** 0
**Started:** 
**Last mentioned to Scott:** never

## Where she is now

(One short paragraph, kept current: chapter or area, party, the story so far in her words.)

## Sessions

| Date | Hours | Where she got to | What happened (real game events) | Her reaction |
| --- | --- | --- | --- | --- |

## What she told Scott, and what he said

| Date | What she said | What he said back |
| --- | --- | --- |
"""


def read():
    return open(NOW).read() if os.path.exists(NOW) else TEMPLATE


def field(s, name):
    m = re.search(rf"^\*\*{re.escape(name)}:\*\* ?(.*)$", s, re.M)
    return m.group(1).strip() if m else ""


def set_field(s, name, value):
    return re.sub(rf"^(\*\*{re.escape(name)}:\*\*).*$", lambda m: f"{m.group(1)} {value}", s, count=1, flags=re.M)


def hours(s):
    try:
        return float(field(s, "Hours played") or 0)
    except ValueError:
        return 0.0


def length(s):
    m = re.search(r"([\d.]+)", field(s, "Length"))
    return float(m.group(1)) if m else 0.0


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    s = read()
    game = field(s, "Game")
    if cmd == "status":
        total = length(s)
        print(f"{game}: {hours(s):g} of about {total:g} hours" + (f" ({hours(s) / total:.0%})" if total else ""))
        rows = [l for l in s.split("\n") if re.match(r"\| \d{4}-", l)]
        print("Last session: " + (rows[-1] if rows else "none yet"))
        print("Last mentioned to Scott: " + field(s, "Last mentioned to Scott"))
        return
    d = dt.date.fromisoformat(sys.argv[2])
    if cmd == "roll":
        weekend = d.weekday() >= 5
        evening = d if weekend else d - dt.timedelta(days=1)   # weekday morning call: last night; weekend call: today
        r = random.Random(f"mizuki-games-{evening.isoformat()}")
        played = r.random() < PLAY[evening.weekday()] or hours(s) == 0   # the evening she starts a new game, she plays it
        hrs = 0.0
        if played:
            hrs = round(r.choice([0.5, 0.75, 1, 1, 1, 1.25, 1.5, 1.5, 2]) if r.random() > 0.05 else 3, 2)
        when = "today" if weekend else f"last night ({evening:%A})"
        if game.startswith("(none"):
            print("No game in memory/now_playing.md yet: pick one (rules in that file) and start it today.")
        elif played:
            print(f"Retro game {when}: she played {game} for about {hrs:g} h. Look up where that gets her from "
                  f"{hours(s):g} h in (real story, no inventing), then: python3 engine/games.py log {evening.isoformat()} {hrs:g} \"...\"")
        else:
            print(f"Retro game {when}: didn't play {game}.")
        if FFXIV[evening.weekday()]:
            print(f"FFXIV {when}: {FFXIV[evening.weekday()]} (memory/ffxiv.md).")
        last = field(s, "Last mentioned to Scott")
        try:
            gap = (d - dt.date.fromisoformat(last[:10])).days
        except ValueError:
            gap = 99
        m = random.Random(f"mizuki-games-mention-{d.isoformat()}").random()
        bring = gap >= 4 or (gap >= 2 and m < 0.6) or (played and hrs >= 2 and gap >= 1)
        print(f"Bring it up on this call: {'yes' if bring else 'no'} (last mentioned {last or 'never'}). "
              "If yes, as a conversation starter: where she's up to, the story or lore so far, how she feels about it.")
        return
    if cmd == "log":
        hrs, where = float(sys.argv[3]), sys.argv[4]
        s = set_field(s, "Hours played", f"{hours(s) + hrs:g}")
        anchor = "| --- | --- | --- | --- | --- |\n"
        i = s.index(anchor) + len(anchor)
        j = s.index("\n## ", i) if "\n## " in s[i:] else len(s)
        block = s[i:j].rstrip("\n")
        row = f"| {d.isoformat()} | {hrs:g} | {where} | | |"
        s = s[:i] + (block + "\n" if block else "") + row + "\n" + s[j:]
        open(NOW, "w").write(s)
        print(f"{game}: now {hours(s):g} of about {length(s):g} hours. Fill in the row's story and her reaction, and 'Where she is now'.")
        return
    if cmd == "mentioned":
        open(NOW, "w").write(set_field(s, "Last mentioned to Scott", d.isoformat()))
        print(f"{game}: mentioned on {d.isoformat()}.")
        return
    if cmd == "finish":
        os.makedirs(DONE, exist_ok=True)
        slug = re.sub(r"[^a-z0-9]+", "-", game.split("(")[0].lower()).strip("-")[:60] or "game"
        dest = f"{DONE}/{d.isoformat()}_{slug}.md"
        done = s.replace("# Now playing", f"# Finished: {game}", 1)
        done = done.replace("**Hours played:**", f"**Finished:** {d.isoformat()}\n**Hours played:**", 1)
        open(dest, "w").write(done)
        open(NOW, "w").write(TEMPLATE)
        print(f"Saved {os.path.relpath(dest, REPO)}; memory/now_playing.md is ready for the next game. Add a line to memory/games_finished/README.md.")
        return
    sys.exit(__doc__)


if __name__ == "__main__":
    main()
