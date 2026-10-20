"""Scott's daily fitness challenges: the tally in memory/challenges.md and his completion rate.

memory/challenges.md is the single source of truth (Scott can edit it on GitHub: set Done to Yes or No).
Commands (dates are YYYY-MM-DD, Sydney time):
  python3 engine/challenges.py add DATE "Challenge text"   # record today's challenge (Done: Not yet)
  python3 engine/challenges.py done DATE yes|no            # record whether he did it
  python3 engine/challenges.py rate [DATE]                 # completion rate over every challenge before DATE
  python3 engine/challenges.py misses DATE                 # how many challenges in a row he missed just before DATE
  python3 engine/challenges.py show                        # print the table
Rate = challenges done / challenges set, counting every challenge before DATE (so not today's). "Not yet" counts
as not done; it rises again as soon as he reports one as done, even late.
"""
import os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = f"{REPO}/memory/challenges.md"
HEADER = """# Daily challenges

One fitness challenge per episode (bible section 8). Scott reports Done on the day's sheet, in a chat or in the inbox; he can also edit Done here (Yes or No). Completion rate = done / challenges set before today, with "Not yet" counted as not done. Use `engine/challenges.py`.

| Date | Challenge | Done |
| --- | --- | --- |
"""


def load():
    rows = []
    if os.path.exists(PATH):
        for line in open(PATH):
            m = re.match(r"\|\s*(\d{4}-\d{2}-\d{2})\s*\|(.*)\|\s*([^|]*?)\s*\|\s*$", line)
            if m:
                rows.append([m.group(1), m.group(2).strip(), m.group(3) or "Not yet"])
    return rows


def save(rows):
    rows.sort(key=lambda r: r[0], reverse=True)
    with open(PATH, "w") as f:
        f.write(HEADER + "".join(f"| {d} | {c.replace('|', '/')} | {s} |\n" for d, c, s in rows))


def rate(rows, before=None):
    past = [r for r in rows if before is None or r[0] < before]
    done = sum(1 for r in past if r[2].lower().startswith("y"))
    return done, len(past)


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "show"
    rows = load()
    if cmd == "add":
        d, text = sys.argv[2], sys.argv[3]
        rows = [r for r in rows if r[0] != d] + [[d, text, "Not yet"]]
        save(rows); print(f"Added {d}: {text}")
    elif cmd == "done":
        d, ans = sys.argv[2], sys.argv[3].lower()
        hit = [r for r in rows if r[0] == d]
        if not hit:
            sys.exit(f"No challenge on {d}")
        hit[0][2] = "Yes" if ans.startswith("y") else "No"
        save(rows); print(f"{d}: {hit[0][2]}")
    elif cmd == "misses":
        past = sorted((r for r in rows if r[0] < sys.argv[2]), key=lambda r: r[0], reverse=True)
        n = 0
        for r in past:
            if r[2].lower().startswith("y"):
                break
            n += 1
        print(f"{n} missed in a row")
    elif cmd == "rate":
        done, total = rate(rows, sys.argv[2] if len(sys.argv) > 2 else None)
        print(f"{done} of {total}, {round(100 * done / total)}%" if total else "No challenges yet")
    else:
        print(open(PATH).read() if os.path.exists(PATH) else "No challenges yet")


if __name__ == "__main__":
    main()
