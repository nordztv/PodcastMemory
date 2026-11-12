"""The day's brief for the daily run: everything that's easy to forget, on one screen.

Usage: python3 engine/preflight.py DATE      (DATE = the episode's date, YYYY-MM-DD)
Prints: the day's special rules, where Mizuki is for each call (bible section 5, The two calls), her usual evening
last night, the dice, the calendar window, the challenge streak, Scott's unanswered questions, open threads that
are due, who sent the last voice notes, the least recently used callbacks, and the word budgets.
It only reads files. Run it at the start of step 2 of show/daily_run.md and again before writing.
"""
import datetime as dt, os, re, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = f"{REPO}/memory"
# Her fixed weekly rhythm (show/mizuki/DIGEST.md, "Her week"). Index = weekday of the EVENING (0 = Monday).
EVENINGS = [
    "Monday evening: FFXIV roulettes or decorating the Free Company house; early night.",
    "Tuesday evening: raid night with Tsukimi Noodles, 9pm (hojicha she forgets to drink). Bed late.",
    "Wednesday evening: lazy night (face mask, a drama); Korean lesson with Lily.",
    "Thursday evening: raid night with Tsukimi Noodles, 9pm. Bed late.",
    "Friday evening: a film, or hitokara in Haymarket when homesick.",
    "Saturday: the fish market ('one good thing'), then Nana's K-pop dance class.",
    "Sunday: parents' video call in the morning; Fiona's brunch monthly; okonomiyaki at night, photo to Mum.",
]
FIXED = {(4, 10): "Mizuki's birthday", (6, 10): "Scott's birthday", (9, 17): "their friendship anniversary",
         (11, 12): "the show's birthday", (12, 25): "Christmas", (11, 22): "Kenta's birthday",
         (1, 21): "Yumiko's birthday", (4, 14): "Hana's birthday", (1, 17): "Hanshin earthquake memorial (quiet line)",
         (11, 15): "Shichi-go-san", (2, 3): "Setsubun", (3, 3): "Hinamatsuri", (7, 7): "Tanabata", (12, 31): "Omisoka",
         (1, 1): "New Year", (10, 10): "Isamu's watch day ('kanpai, Jiichan')", (9, 18): "Aya's birthday"}
BUDGET = {"01": 700, "02": 1200, "03": 1400, "04": 1800, "05": 1400, "06": 1100, "07": 450, "08": 800, "09": 800,
          "10": 400, "11": 900}


def read(name):
    try:
        return open(f"{M}/{name}").read()
    except OSError:
        return ""


def rows(text):
    out = []
    for line in text.splitlines():
        if line.startswith("|") and not re.match(r"\|\s*-", line):
            out.append([c.strip() for c in line.strip().strip("|").split("|")])
    return out


def run(*args):
    return subprocess.run([sys.executable, *args], capture_output=True, text=True, cwd=REPO).stdout.strip()


def main():
    d = dt.date.fromisoformat(sys.argv[1])
    wd = d.weekday()
    prev = d - dt.timedelta(days=1)
    print(f"=== Brief for {d.strftime('%A %d %B %Y')} ===\n")

    print("TODAY'S SPECIAL RULES")
    if wd == 0:
        print("- Monday: news since Friday; her weekend (roll Sat and Sun too); Retro Game of the Week pick; new Actress of the Week.")
    if wd == 1:
        print("- Tuesday: a quick nudge on the retro game.")
    if wd == 2:
        print("- Wednesday: retro game retrospective; Yokai of the Week or a Pokemon moment in the chat.")
    if wd == 4:
        print("- Friday: weekend send-off chat (about 1,800 words), photo of the week, weekend ideas, defending the picks, project check-in, weekly review.")
        if (d + dt.timedelta(days=7)).month != d.month:
            print("- Last Friday of the month: Photo of the Month.")
    recent = read("recent_episodes.md")
    if f"## {d.strftime('%Y-%m')}" not in recent:
        print("- FIRST EPISODE OF THE MONTH: monthly rollover, opportunity roll, a new modest goal, monthly check-in in the chat.")
    if wd in (1, 3):
        print("- An ordinary weekday: no fixed feature, so her day and his answers carry it.")

    print("\nTHE TWO CALLS (bible section 5)")
    print(f"- Morning call (about 8am {d.strftime('%A')}): she's at home in Pyrmont before work (leaves 10:10): breakfast, tea, the balcony.")
    print(f"  What she can talk about: last night -> {EVENINGS[prev.weekday()]}")
    if wd == 0:
        print("  Plus the whole weekend (Saturday and Sunday rhythms above; her plans are in memory/mizuki.md, Her weekends).")
    print(f"- Afternoon call (about 4pm {d.strftime('%A')}): the shop's quiet hour; she steps out the back or walks to the bank.")
    print("  What she can talk about: this morning's walk over Pyrmont Bridge and today's lunch rush. Tonight hasn't happened yet.")
    print(f"  Tonight for her -> {EVENINGS[wd]} (she can look forward to it; she reports on it tomorrow)")
    print("- She only knows news up to when the run happens (the evening before). Never 'this morning's news'.")

    print("\nDICE")
    dates = [d.isoformat()] if wd else [(d - dt.timedelta(days=2)).isoformat(), prev.isoformat(), d.isoformat()]
    print(run("engine/life_dice.py", *dates))
    en = re.search(r"\*\*Now: (\d+) out of 10\*\*", read("mizuki_life.md"))
    print(f"Energy yesterday: {en.group(1) if en else '?'} of 10 (move it a step or two, with a reason).")

    print("\nCALENDAR, NEXT 7 DAYS")
    hit = False
    for i in range(8):
        x = d + dt.timedelta(days=i)
        if (x.month, x.day) in FIXED:
            hit = True
            print(f"- {x.strftime('%a %d %b')}: {FIXED[(x.month, x.day)]}")
    if not hit:
        print("- No fixed dates. Still read this month's section of show/mizuki/CALENDAR.md (seasons, festivals, FFXIV).")

    print("\nCHALLENGE")
    print("- Rate: " + run("engine/challenges.py", "rate", d.isoformat()) + " | " + run("engine/challenges.py", "misses", d.isoformat()))
    last = [r for r in rows(read("challenges.md")) if re.match(r"\d{4}-", r[0])][:5]
    print("- Recent (don't repeat): " + "; ".join(r[1] for r in last))

    print("\nSCOTT")
    q = [r for r in rows(read("questions.md")) if re.match(r"\d{4}-", r[0])]
    waiting = [r for r in q if r[3].lower().startswith("not yet")]
    print(f"- Questions waiting on him: {len(waiting)} (never nag; after 5 days let one go quietly).")
    todo = [r for r in q if not r[3].lower().startswith("not yet") and r[4].lower() == "no"]
    for r in todo:
        print(f"- ANSWER TO REACT TO: {r[1]} -> {r[3]}")

    print("\nOPEN THREADS DUE (memory/open_threads.md)")
    any_due = False
    for r in rows(read("open_threads.md")):
        if len(r) >= 5 and re.match(r"\d{4}-\d\d-\d\d", r[2]) and r[4].lower().startswith("open"):
            if dt.date.fromisoformat(r[2][:10]) <= d:
                any_due = True
                print(f"- [{r[0]}] {r[1]} (due {r[2]}; {r[3]})")
    if not any_due:
        print("- Nothing due today.")

    print("\nVARIETY")
    vn = [r for r in rows(read("voice_notes.md")) if re.match(r"\d{4}-", r[0])]
    week = [r for r in vn if dt.date.fromisoformat(r[0]) > d - dt.timedelta(days=7)]
    print(f"- Voice notes in the last 7 days: {len(week)} (aim for about 2 a week). Last from: {vn[0][1] if vn else 'nobody yet'}.")
    mem = [r for r in rows(read("memories_told.md")) if re.match(r"\d{4}-", r[0])][:3]
    print("- Last memories told: " + "; ".join(r[1][:60] for r in mem))
    cb = sorted((r for r in rows(read("callbacks.md")) if len(r) >= 3 and re.match(r"\d{4}-", r[2])), key=lambda r: r[2])[:4]
    print("- Callbacks not used lately: " + "; ".join(f"{r[0]} ({r[2]})" for r in cb))
    taught = [r for r in rows(read("scott_taught_me.md")) if re.match(r"\d{4}-", r[0]) and not r[3]]
    if taught:
        print("- Things he taught her she hasn't followed up: " + "; ".join(r[1][:50] for r in taught[:3]))

    print("\nWORD BUDGETS (check_script.py reports the real counts)")
    b = dict(BUDGET)
    if wd == 4:
        b["11"], b["08"], b["09"] = 1800, 650, 650
    print("- " + ", ".join(f"{k}: {v}" for k, v in b.items()) + f" = about {sum(b.values()):,} words")


if __name__ == "__main__":
    main()
