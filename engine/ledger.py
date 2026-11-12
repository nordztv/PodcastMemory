"""Mizuki's money, kept honest: every dollar in or out of her savings funds is a dated line in a ledger.

Usage:
  python3 engine/ledger.py check                               # do the funds in memory/mizuki_life.md add up to the total?
  python3 engine/ledger.py move DATE AMOUNT "Fund" "what for"  # AMOUNT can be negative (spending) or positive (saving)
`move` changes that fund's "Saved" figure and the total in memory/mizuki_life.md, refuses to take a fund below zero,
and appends a line to memory/mizuki_ledger.md. Everyday spending inside her weekly budget (groceries, coffee) isn't
logged here; only money into or out of a fund. The emergency fund is for emergencies only: say why in "what for".
"""
import os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIFE, LEDGER = f"{REPO}/memory/mizuki_life.md", f"{REPO}/memory/mizuki_ledger.md"
ROW = re.compile(r"^\| (?P<fund>[^|*]+?) \| \$(?P<saved>[\d,]+) \| (?P<rest>.*)$")
TOTAL = re.compile(r"^\| \*\*Total\*\* \| \*\*\$([\d,]+)\*\* \|")


def funds(lines):
    """Only the rows of the table under the "## Savings" heading (the weekly budget table has dollar figures too)."""
    start = next(i for i, l in enumerate(lines) if l.startswith("## Savings"))
    end = next(i for i, l in enumerate(lines) if i > start and l.startswith("## "))
    return {m["fund"]: (i, int(m["saved"].replace(",", ""))) for i, l in enumerate(lines)
            if start < i < end and (m := ROW.match(l))}


def main():
    lines = open(LIFE).read().split("\n")
    f = funds(lines)
    ti = next(i for i, l in enumerate(lines) if TOTAL.match(l))
    total = int(TOTAL.match(lines[ti]).group(1).replace(",", ""))
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "check":
        s = sum(v for _, v in f.values())
        for name, (_, v) in f.items():
            print(f"{name}: ${v:,}")
        print(f"Funds add up to ${s:,}; stated total ${total:,}: " + ("OK" if s == total else "MISMATCH, fix it"))
        return 0 if s == total else 1
    if cmd == "move":
        date, amount, fund, what = sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5]
        key = next((k for k in f if k.lower() == fund.lower()), None)
        if not key:
            sys.exit(f"No fund called {fund!r}. Funds: {', '.join(f)}")
        i, v = f[key]
        if v + amount < 0:
            sys.exit(f"{key} only has ${v:,}: she can't spend ${-amount:,} from it.")
        lines[i] = lines[i].replace(f"| ${v:,} |", f"| ${v + amount:,} |", 1)
        lines[ti] = lines[ti].replace(f"${total:,}", f"${total + amount:,}", 1)
        open(LIFE, "w").write("\n".join(lines))
        with open(LEDGER, "a") as out:
            out.write(f"| {date} | {what} | {'+' if amount >= 0 else '-'}${abs(amount):,} | {key} | ${v + amount:,} | ${total + amount:,} |\n")
        print(f"{key}: ${v:,} -> ${v + amount:,}. Total ${total + amount:,}.")
        return 0
    sys.exit(__doc__)


if __name__ == "__main__":
    sys.exit(main())
