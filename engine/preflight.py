"""The day's brief for the daily run: everything that's easy to forget, on one screen.

Usage: python3 engine/preflight.py DATE      (DATE = the call day's date, YYYY-MM-DD)
Prints: what's different about the day (guidance only), where Mizuki is for each call (bible section 5, The two calls), her usual evening
last night, the dice, the calendar window, the challenge streak, Scott's unanswered questions, open threads that
are due, who sent the last voice notes, the least recently used callbacks, hellos used lately, and how long the calls might run.
It only reads files. Run it at the start of step 2 of show/daily_run.md and again before writing.
"""
import datetime as dt, glob, os, re, subprocess, sys

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
         (11, 12): "the anniversary of her first call to Scott", (12, 25): "Christmas", (11, 22): "Kenta's birthday",
         (1, 21): "Yumiko's birthday", (4, 14): "Hana's birthday", (1, 17): "Hanshin earthquake memorial (quiet line)",
         (11, 15): "Shichi-go-san", (2, 3): "Setsubun", (3, 3): "Hinamatsuri", (7, 7): "Tanabata", (12, 31): "Omisoka",
         (1, 1): "New Year", (10, 10): "Isamu's watch day ('kanpai, Jiichan')", (9, 18): "Aya's birthday"}


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

    print("TODAY (guidance, not a checklist: bible section 0, Loose, not scripted)")
    if wd == 0:
        print("- Monday: she spoke to him on Sunday evening, so there's no weekend to retell; news since then if any.")
    if wd == 4:
        print("- Friday: the 4pm call usually drifts into weekend talk (her plans, his, maybe an idea or two for him); the weekly review is behind the scenes.")
    # The first WEEKDAY of a month (weekend calls don't count): the 3am morning run does the rollover.
    first = d.replace(day=1)
    while first.weekday() >= 5:
        first += dt.timedelta(days=1)
    if d == first:
        print("- FIRST WEEKDAY OF THE MONTH: morning run: monthly rollover, opportunity roll, a new modest goal. She might check in on him in a bigger way this week.")
    print("- What's on her mind is up to her day: her life, him, the things they both love, the news only if it's worth talking about.")
    things = []
    for f, label in (("retro_games.md", "the retro game she wants him to play"), ("actress_of_the_week.md", "the actress she's into")):
        r = [x for x in rows(read(f)) if re.match(r"\d{4}-", x[0])]
        if r:
            things.append(f"{label}: {r[0][1]}" + (f" ({r[0][2]})" if len(r[0]) > 2 and f.startswith("actress") else ""))
    if things:
        print("- Things she's into this week (bring up when she feels like it): " + "; ".join(things))
    if True:
        greet = []
        for back in range(1, 6):
            p_ = d - dt.timedelta(days=back)
            for g_ in sorted(glob.glob(f"{REPO}/archive/{p_:%Y/%m}/{p_.isoformat()}/script/*.txt")):
                n_ = os.path.basename(g_)
                if re.match(r"^(am|pm|eve)_0*1_", n_) or n_ in ("01_opening_world.txt", "07_walkhome.txt", "01_evening_hello.txt"):
                    first_line = re.sub(r"\[[^\]]*\]", "", open(g_).read()).strip().split("\n")[0]
                    greet.append(f"{p_:%a}: \"{' '.join(first_line.split()[:9])}\"")
        if greet:
            print("- Hellos she used lately (never the same twice running): " + " | ".join(greet[:6]))

    if wd >= 5:
        print("- WEEKEND: one call at 7pm (her time), usually 10 to 25 minutes, her own hello, no challenge unless it comes up. Follow show/weekend_run.md.")
        print(f"  Her day -> {EVENINGS[wd]}")
        print("  The run happens at about 4pm: she knows the real world only up to then; her own evening is hers to tell.")
    if wd < 5:
        print("\nTHE TWO CALLS (bible section 5; weekdays only)")
        print(f"- Morning call (about 8am {d.strftime('%A')}): she's at home in Pyrmont before work (leaves 10:10): breakfast, tea, the balcony.")
        last = "Sunday night, after their 7pm call (she already told him about her Sunday); her week ahead." if wd == 0 else EVENINGS[prev.weekday()]
        print(f"  What she can talk about: last night -> {last}")
        print(f"- Afternoon call (about 4pm {d.strftime('%A')}): the shop's quiet hour; she steps out the back or walks to the bank.")
        print("  What she can talk about: this morning's walk over Pyrmont Bridge and today's lunch rush. Tonight hasn't happened yet.")
        print(f"  Tonight for her -> {EVENINGS[wd]} (she can look forward to it; she reports on it tomorrow)")
        print("- Morning call: written at about 3am, so she knows the news up to then ('last night', 'when I woke up'). Afternoon call: up to lunchtime ('on my break').")

    print("\nDICE")
    dates = [d.isoformat()]   # Saturday and Sunday are rolled by their own weekend runs
    print(run("engine/life_dice.py", *dates))
    rows_e = sorted(m.groups() for m in re.finditer(r"^\| (\d{4}-\d\d-\d\d) \| (\d+) \|", read("mizuki_life.md"), re.M))
    before = [r for r in rows_e if r[0] < d.isoformat()]
    today_row = [r for r in rows_e if r[0] == d.isoformat()]
    if today_row:
        print(f"Energy today: {today_row[0][1]} of 10 (already set for {d.isoformat()}).")
    elif before:
        print(f"Energy last set: {before[-1][1]} of 10 on {before[-1][0]} (move it a step or two a day, with a reason, and add a row for {d.isoformat()}).")

    print("\nCALENDAR, NEXT 7 DAYS")
    hit = False
    for i in range(8):
        x = d + dt.timedelta(days=i)
        if (x.month, x.day) in FIXED:
            hit = True
            print(f"- {x.strftime('%a %d %b')}: {FIXED[(x.month, x.day)]}")
    if not hit:
        print("- No fixed dates. Still read this month's section of show/mizuki/CALENDAR.md (seasons, festivals, FFXIV).")

    if wd < 5:
        print("\nCHALLENGE (only when it comes up: bible section 8)")
        last = [r for r in rows(read("challenges.md")) if re.match(r"\d{4}-", r[0])][:5]
        if last:
            print(f"- Last one: {last[0][1]} ({last[0][0]}, done: {last[0][2]}). Set one only if it fits today; a couple a week at most.")

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

    if wd >= 5:
        print("\nLENGTH: usually 10 to 25 minutes (about 1,400 to 3,400 words), shorter when she's tired.")
        return
    en_now = int(today_row[0][1]) if today_row else int(before[-1][1]) if before else 6
    print("\nLENGTH (bible section 5, Length)")
    print("- Each weekday call: 40 to 50 minutes (about 5,400 to 6,700 words), the morning call and the 4pm call alike.")
    print(f"- Her energy is {en_now}: " + ("low, so nearer 40 minutes; she says she's tired." if en_now <= 4 else "bright, so nearer 50; she rambles." if en_now >= 8 else "an ordinary day."))

if __name__ == "__main__":
    main()
