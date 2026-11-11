"""Rolls the dice for Mizuki's week, so her life has real ups and downs instead of always going well.

Usage: python3 engine/life_dice.py WEEK_ENDING_DATE
Prints one roll per day (Monday to Sunday) and a week roll. The Sunday run (show/daily_run.md, step 2b) turns each
roll into something realistic that fits her life, money and history (memory/mizuki_life.md, memory/mizuki_timeline.md,
show/mizuki_history.md). Seeded by the date, so re-running gives the same rolls.

Day roll (d20):  1 = a real setback   2-5 = a small bad thing   6-16 = an ordinary day
                17-19 = a nice surprise   20 = something lovely
Week roll (d100): 1-4 = a significant bad event (illness, a big bill, a family worry, a job problem)
                  5-92 = nothing big     93-100 = a significant good event (a win, an opportunity, a goal jumps ahead)
"""
import datetime, random, sys

DAY = [(1, "a real setback"), (5, "a small bad thing"), (16, "an ordinary day"), (19, "a nice surprise"), (20, "something lovely")]
WEEK = [(4, "a significant bad event"), (92, "nothing big"), (100, "a significant good event")]


def label(table, roll):
    return next(text for top, text in table if roll <= top)


def main():
    end = datetime.date.fromisoformat(sys.argv[1])
    rng = random.Random(f"mizuki-{end.isoformat()}")
    for i in range(7):
        day = end - datetime.timedelta(days=6 - i)
        r = rng.randint(1, 20)
        print(f"{day.strftime('%a %d %b')}: d20 {r:2d}  {label(DAY, r)}")
    w = rng.randint(1, 100)
    print(f"Week: d100 {w:3d}  {label(WEEK, w)}")


if __name__ == "__main__":
    main()
