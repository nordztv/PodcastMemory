"""Scott's topic scores: keeps memory/topics.md tidy and applies the scoring rules.

memory/topics.md is the single source of truth (Scott can edit it directly on GitHub).
Commands (dates are YYYY-MM-DD, Sydney time):
  python3 engine/topics.py signal "Topic name" POINTS DATE   # add points; creates the topic as minor at 10 first if new
  python3 engine/topics.py hot "Topic name" UNTIL_DATE        # mark a topic hot until a date (creates it if new)
  python3 engine/topics.py daily DATE                         # once a day: fading, expire hot flags, promote, cap, sort
  python3 engine/topics.py show                               # print the current tables
Topic names match case-insensitively; use the exact name from topics.md where possible.
"""
import datetime as dt
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = f"{REPO}/memory/topics.md"
MAIN_SIZE, MINOR_CAP, NEW_SCORE, FADE_AFTER, FADE_BY = 25, 100, 10, 14, 2

HEADER = """# Scott's topics

The 25 highest-scoring topics are main topics: they get most of the airtime and drive the deep dives. Up to 100 more are minor topics: a brief mention at most, unless hot. Scoring rules are in `show/bible.md`. Scott can edit any row here directly; keep the table format and use YYYY-MM-DD dates.

Last daily update: {last}
"""
ROW = "| {topic} | {score} | {last} | {hot} |"
TABLE_HEAD = "| Topic | Score | Last signal | Hot until |\n| --- | --- | --- | --- |"


def load():
    text = open(PATH).read()
    m = re.search(r"Last daily update: (\S+)", text)
    last_daily = m.group(1) if m else "never"
    rows = []
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 4 and cells[0] not in ("Topic", "---") and not set(cells[0]) <= {"-"}:
            try:
                rows.append({"topic": cells[0], "score": int(cells[1]), "last": cells[2], "hot": cells[3]})
            except ValueError:
                pass
    return rows, last_daily


def save(rows, last_daily):
    rows.sort(key=lambda r: (-r["score"], r["topic"].lower()))
    main, minor = rows[:MAIN_SIZE], rows[MAIN_SIZE:]
    minor.sort(key=lambda r: (-r["score"], r["last"] == "" , r["last"]), reverse=False)
    # cap: drop lowest score, oldest signal first
    while len(minor) > MINOR_CAP:
        worst = min(minor, key=lambda r: (r["score"], r["last"] or "0000"))
        minor.remove(worst)
    minor.sort(key=lambda r: (-r["score"], r["topic"].lower()))
    out = [HEADER.format(last=last_daily),
           "## Main topics (top 25)\n", TABLE_HEAD] + [ROW.format(**r) for r in main]
    out += ["", "## Minor topics (up to 100)\n", TABLE_HEAD] + [ROW.format(**r) for r in minor]
    open(PATH, "w").write("\n".join(out) + "\n")


def find(rows, name):
    for r in rows:
        if r["topic"].lower() == name.lower():
            return r
    return None


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "show"
    rows, last_daily = load()
    if cmd == "signal":
        name, pts, date = sys.argv[2], int(sys.argv[3]), sys.argv[4]
        r = find(rows, name)
        if not r:
            r = {"topic": name, "score": NEW_SCORE, "last": date, "hot": ""}
            rows.append(r)
            print(f"added new topic: {name}")
        r["score"] = max(0, min(100, r["score"] + pts))
        r["last"] = max(r["last"], date) if r["last"] else date
        print(f"{r['topic']}: {r['score']}")
    elif cmd == "hot":
        name, until = sys.argv[2], sys.argv[3]
        r = find(rows, name)
        if not r:
            r = {"topic": name, "score": NEW_SCORE, "last": until, "hot": ""}
            rows.append(r)
        r["hot"] = until
        print(f"{r['topic']} hot until {until}")
    elif cmd == "daily":
        date = sys.argv[2]
        if last_daily == date:
            print("daily already applied today")
        else:
            today = dt.date.fromisoformat(date)
            for r in rows:
                try:
                    if (today - dt.date.fromisoformat(r["last"])).days > FADE_AFTER:
                        r["score"] = max(0, r["score"] - FADE_BY)
                except ValueError:
                    pass
                if r["hot"]:
                    try:
                        if dt.date.fromisoformat(r["hot"]) < today:
                            r["hot"] = ""
                    except ValueError:
                        r["hot"] = ""
            last_daily = date
            print("daily applied")
    elif cmd != "show":
        print(__doc__)
        return
    save(rows, last_daily)
    if cmd == "show":
        print(open(PATH).read())


if __name__ == "__main__":
    main()
