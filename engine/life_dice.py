"""Rolls the dice for Mizuki's life, so it has real ups and downs instead of always going well.

Usage: python3 engine/life_dice.py DATE [DATE ...]
For each date, prints that day's roll, and whether this week's big event (if the week has one) lands that day.
Every daily run rolls its episode's date (and on Mondays also the Saturday and Sunday before), turns the result into
something realistic that fits her life, money and history, and she tells Scott about it in that episode. Nothing is
decided ahead, so her timeline never contains spoilers. Seeded by the date, so re-running gives the same result.

Day roll (d20):  1 = a real setback   2-5 = a small bad thing   6-16 = an ordinary day
                17-19 = a nice surprise   20 = something lovely
Week roll (d100, once per Monday-to-Sunday week, landing on one random day):
                 1-4 = a significant bad event (illness, a big bill, a family worry, a job problem)
                 5-92 = nothing big     93-100 = a significant good event (a win, an opportunity, a goal jumps ahead)
"""
import datetime, random, sys

DAY = [(1, "a real setback"), (5, "a small bad thing"), (16, "an ordinary day"), (19, "a nice surprise"), (20, "something lovely")]
WEEK = [(4, "a significant bad event"), (92, None), (100, "a significant good event")]


def label(table, roll):
    return next(text for top, text in table if roll <= top)


def roll(date):
    r = random.Random(f"mizuki-day-{date.isoformat()}").randint(1, 20)
    monday = date - datetime.timedelta(days=date.weekday())
    wr = random.Random(f"mizuki-week-{monday.isoformat()}")
    w, wday = wr.randint(1, 100), wr.randint(0, 6)
    week_event = label(WEEK, w) if wday == date.weekday() else None
    return r, week_event


def main():
    for arg in sys.argv[1:]:
        d = datetime.date.fromisoformat(arg)
        r, ev = roll(d)
        line = f"{d.strftime('%a %d %b %Y')}: d20 {r:2d}  {label(DAY, r)}"
        if ev:
            line += f"   + THIS WEEK'S BIG EVENT LANDS TODAY: {ev}"
        print(line)


if __name__ == "__main__":
    main()
