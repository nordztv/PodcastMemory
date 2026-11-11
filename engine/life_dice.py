"""Rolls the dice for Mizuki's life, so it has real ups and downs instead of always going well.

Usage: python3 engine/life_dice.py DATE [DATE ...]
For each date, prints that day's roll, and whether this week's big event or this week's news from someone in her
life (if the week has either) lands that day.

       python3 engine/life_dice.py arcs SUNDAY_DATE "Arc name" ["Arc name" ...]
Sunday runs only: rolls each active long story arc in memory/mizuki_arcs.md once for the week ending that Sunday.
Every daily run rolls its episode's date (and on Mondays also the Saturday and Sunday before), turns the result into
something realistic that fits her life, money and history, and she tells Scott about it in that episode. Nothing is
decided ahead, so her timeline never contains spoilers. Seeded by the date, so re-running gives the same result.

Day roll (d20):  1 = a real setback   2-5 = a small bad thing   6-16 = an ordinary day
                17-19 = a nice surprise   20 = something lovely
Week roll (d100, once per Monday-to-Sunday week, landing on one random day):
                 1-4 = a significant bad event (illness, a big bill, a family worry, a job problem)
                 5-92 = nothing big     93-100 = a significant good event (a win, an opportunity, a goal jumps ahead)
People roll (d100, once per week, landing on one random day; Scott's feature 10, 12 Nov 2026):
                 1-25 = someone in her life has news this week (the run picks who fits memory/people_timelines.md),
                        with a tone (d6): 1 = bad news   2-4 = everyday news   5-6 = good news
Arc roll (d20 per active arc, Sundays; Scott's feature 9):
                 1-2 = a setback   3-12 = no real change   13-18 = a step forward   19-20 = a big leap
"""
import datetime, random, sys

DAY = [(1, "a real setback"), (5, "a small bad thing"), (16, "an ordinary day"), (19, "a nice surprise"), (20, "something lovely")]
WEEK = [(4, "a significant bad event"), (92, None), (100, "a significant good event")]
TONE = [(1, "bad news"), (4, "everyday news"), (6, "good news")]
ARC = [(2, "a setback"), (12, "no real change"), (18, "a step forward"), (20, "a big leap")]


def label(table, roll):
    return next(text for top, text in table if roll <= top)


def roll(date):
    r = random.Random(f"mizuki-day-{date.isoformat()}").randint(1, 20)
    monday = date - datetime.timedelta(days=date.weekday())
    wr = random.Random(f"mizuki-week-{monday.isoformat()}")
    w, wday = wr.randint(1, 100), wr.randint(0, 6)
    week_event = label(WEEK, w) if wday == date.weekday() else None
    pr = random.Random(f"mizuki-people-{monday.isoformat()}")
    p, pday, tone = pr.randint(1, 100), pr.randint(0, 6), pr.randint(1, 6)
    people = label(TONE, tone) if p <= 25 and pday == date.weekday() else None
    return r, week_event, people


def main():
    if sys.argv[1:2] == ["arcs"]:
        d = datetime.date.fromisoformat(sys.argv[2])
        for name in sys.argv[3:]:
            a = random.Random(f"mizuki-arc-{d.isoformat()}-{name.lower()}").randint(1, 20)
            print(f"{name}: d20 {a:2d}  {label(ARC, a)}")
        return
    for arg in sys.argv[1:]:
        d = datetime.date.fromisoformat(arg)
        r, ev, people = roll(d)
        line = f"{d.strftime('%a %d %b %Y')}: d20 {r:2d}  {label(DAY, r)}"
        if ev:
            line += f"   + THIS WEEK'S BIG EVENT LANDS TODAY: {ev}"
        if people:
            line += f"   + NEWS FROM SOMEONE IN HER LIFE TODAY: {people}"
        print(line)


if __name__ == "__main__":
    main()
