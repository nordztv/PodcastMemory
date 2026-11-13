"""Weekly consistency audit of Mizuki's life (Sunday runs; Scott's choice, 13 Nov 2026).

Usage: python3 engine/audit_mizuki.py SUNDAY_DATE
More than fifteen files about her change every night, so small contradictions creep in. This checks the things a
machine can check, over her memory files and the last seven days of scripts, and prints CHECK lines. The Sunday evening run
then reads each one, fixes what's really wrong (in the memory file, or with an on-the-phone correction on Monday if she
said it to Scott), and logs the result in memory/audit_log.md. Canon order: show/mizuki/SPINE.md, RESOLUTIONS.md,
the chapters, then people pages.
"""
import datetime as dt, glob, os, re, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORDS = "zero one two three four five six seven eight nine ten eleven twelve".split()
TENS = {30: "thirty"}
# Things canon says are NOT true (show/mizuki/DIGEST.md section 9). A match isn't always wrong ("I've never been
# to Uluru" is fine): each is a line to read.
RED_FLAGS = [
    (r"\bUluru\b", "she has never been to Uluru ('saving it')"),
    (r"\bwaitress\b", "she's the shift lead, not a waitress"),
    (r"\bclarinet\b", "Aya plays the trumpet"),
    (r"\bPentax\b", "Ms Kuroda's camera is an Olympus OM-1"),
    (r"\b(sitting|sat|lying|asleep|curled up) on (my|the) (sofa|couch)\b|\bmy (sofa|couch) (is|was)\b", "she has never owned a sofa in Sydney (unless she has now bought one: check the ledger)"),
    (r"\bparents (visited|came to|were in) Sydney\b", "her parents have never visited Sydney (until the arc says so)"),
    (r"\bI (went )?skydiv", "Nana skydived; Mizuki never has"),
    (r"\bTwelve Apostles\b", "she never saw them (fog)"),
    (r"\bFM2\b[^.\n]{0,50}\b(in|back in) (Osaka|Abeno)\b", "the FM2 is in Pyrmont"),
    (r"\bshoyu lady\b[^.\n]{0,60}\b(died|passed)", "the Monday shoyu lady is alive"),
    (r"\b(just|only) (got|came) home from (the shop|work)\b", "check the two-call timing: in the morning she hasn't worked yet"),
    (r"\bmy (boyfriend|husband|girlfriend)\b", "she's single"),
    (r"\bFumiko (says|said yesterday|called|texted)\b|\bmy grandmother Fumiko (is|was) (visiting|coming)", "Fumiko died in December 2016"),
    (r"\bIsamu (called|texted|is visiting)\b", "Isamu died in February 2005"),
]


def number(n):
    return WORDS[n] if n < len(WORDS) else f"{TENS[n // 10 * 10]} {WORDS[n % 10]}".strip() if n // 10 * 10 in TENS else str(n)


def main():
    end = dt.date.fromisoformat(sys.argv[1])
    start = end - dt.timedelta(days=6)
    found = 0

    def check(msg):
        nonlocal found
        found += 1
        print("CHECK " + msg)

    # 1. money
    r = subprocess.run([sys.executable, f"{REPO}/engine/ledger.py", "check"], capture_output=True, text=True)
    if r.returncode:
        check("her savings funds don't add up to the stated total:\n" + r.stdout.strip())

    # 2. energy moves a step or two a day, and every call day has a row
    life = open(f"{REPO}/memory/mizuki_life.md").read()
    energy = sorted((m.group(1), int(m.group(2))) for m in re.finditer(r"^\| (\d{4}-\d\d-\d\d) \| (\d+) \|", life, re.M))
    for (d1, e1), (d2, e2) in zip(energy, energy[1:]):
        gap = (dt.date.fromisoformat(d2) - dt.date.fromisoformat(d1)).days
        if abs(e2 - e1) > 2 * max(1, gap) and dt.date.fromisoformat(d2) >= start:
            check(f"energy jumps from {e1} ({d1}) to {e2} ({d2}): a step or two a day at most")
    edates = {d for d, _ in energy}

    # 3. every day of the week left a trace in her timeline, and what she said on the phone is canon
    timeline = open(f"{REPO}/memory/mizuki_timeline.md").read()
    age = end.year - 1990 - ((end.month, end.day) < (4, 10))
    years = end.year - 2018 - (end.month < 3)
    texts = {}
    for i in range(7):
        d = start + dt.timedelta(days=i)
        ep = f"{REPO}/archive/{d:%Y/%m}/{d.isoformat()}"
        files = sorted(glob.glob(f"{ep}/script/*.txt"))
        if not files:
            continue
        if f"{d:%a} {d.day} {d:%b}" not in timeline:
            check(f"no line for {d:%a} {d.day} {d:%b} in memory/mizuki_timeline.md, but she rang him that day")
        if d.isoformat() not in edates:
            check(f"no energy row for {d.isoformat()} (the voice reads it)")
        for f in files:
            texts[os.path.relpath(f, REPO)] = open(f).read()
    for name in ["mizuki.md", "mizuki_life.md", "mizuki_timeline.md", "mizuki_home.md", "mizuki_arcs.md",
                 "people_timelines.md", "mizuki_opinions.md"]:
        body = open(f"{REPO}/memory/{name}").read()
        # only the lines dated this week, so old, already-checked lines aren't re-read every Sunday
        recent = [l for l in body.split("\n") if any((start + dt.timedelta(days=i)).isoformat() in l for i in range(7))]
        texts[f"memory/{name}"] = "\n".join(recent)
    for where, text in texts.items():
        plain = re.sub(r"\[[^\]]*\]", " ", text)
        for pat, why in RED_FLAGS:
            for m in re.finditer(pat, plain, re.I):
                line = plain[max(0, m.start() - 70): m.end() + 50].replace("\n", " ")
                check(f"{where}: ...{line.strip()}... ({why})")
        for m in re.finditer(r"\bI(?:'m| am) (thirty[ -]\w+|\d\d)\b", plain):
            if m.group(1).replace("-", " ") not in (number(age), str(age)):
                check(f"{where}: says \"{m.group(0)}\" but she is {age}")
        for m in re.finditer(r"\b(\w+) years (?:in|living in) (?:Sydney|Australia)\b", plain, re.I):
            if m.group(1).lower() in WORDS and m.group(1).lower() != number(years) and m.group(1).lower() != "many":
                check(f"{where}: \"{m.group(0)}\" but it's {number(years)} years (since March 2018)")

    # 4. people and threads
    vn = [l.split("|")[2].strip() for l in open(f"{REPO}/memory/voice_notes.md").read().split("\n") if re.match(r"\| \d{4}-", l)]
    if len(vn) > 1 and vn[0].split(" ")[0] == vn[1].split(" ")[0]:
        check(f"the last two voice notes are both from {vn[0]}")
    try:
        for l in open(f"{REPO}/memory/open_threads.md").read().split("\n"):
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            if len(c) >= 5 and re.match(r"\d{4}-\d\d-\d\d", c[2]) and c[4].lower().startswith("open"):
                if (end - dt.date.fromisoformat(c[2][:10])).days > 7:
                    check(f"open thread a week overdue: [{c[0]}] {c[1]} (due {c[2]}): keep it, or close it with a reason")
    except OSError:
        pass

    print(f"\n{found} thing(s) to read." if found else "Nothing found. Still read this week's scripts against show/mizuki/SPINE.md for anything a pattern can't catch.")


if __name__ == "__main__":
    main()
