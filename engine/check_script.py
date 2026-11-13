"""Pre-recording check of a day's script: words the voice engine could say the wrong way, and name overuse.

Usage: python3 engine/check_script.py YYYY-MM-DD am|pm|eve   (the call to check: the files am_*, pm_* or eve_* in
       the day's script folder; with no call it checks every file)
For every word that's spelled the same but said two ways (live, read, close...) and that show/heteronyms.json didn't
already settle from context, prints the sentence and what the engine will say by default. If that's the wrong one,
write {word|respelling} in the script (for example {live|lyve}, {read|red}, {close|kloze}). Also counts "Scott".

Then a realism check (bible sections 0, 3 and 5): show words that break her world, a hello repeated from a recent
call, phrases that break the two-call timing, repeated little reactions, tags the voice would drop, and how long,
how tagged and how jokey each call is. "CHECK" lines need a look; "FIX" lines must be fixed before committing.
"""
import glob, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tts  # noqa: E402  (reuses its rules; loads no voice model)

DEFAULTS = {  # what the engine says when nothing settles it
    "live": "LIV (to live), unless after is/now/went or before stream, blog, music...",
    "read": "REED (present tense), unless after have/had/was/already...",
    "lead": "LEED (to lead)", "wind": "WIND (the weather)", "wound": "WOOND (an injury)",
    "close": "KLOHS (near), unless after to/will/please... or before the/its/down...",
    "tear": "TEER (crying)", "tears": "TEERS (crying)", "row": "ROH (a line), unless a political or funding row...",
    "minute": "MIN-it (sixty seconds)", "present": "PREZ-ent (now, or a gift)", "content": "KON-tent (material)",
    "record": "REK-ord (the noun) or rih-KORD (the verb), guessed from context", "object": "OB-ject (a thing)",
    "produce": "pruh-DOOCE (to make)", "refuse": "rih-FYOOZ (to say no)", "desert": "DEZ-ert (sand)",
    "bow": "BOH (a ribbon or weapon)", "bass": "BAYSS (music)", "polish": "POL-ish (to shine)",
    "used": "YOOZD (it is used to make), unless I used to, get used to...", "lives": "LYVZ (plural of life), unless she lives in...",
}
WORDS = re.compile(r"\b(" + "|".join(k for k in DEFAULTS if k.isalpha()) + r")\b", re.I)


# At about 135 words a minute (bible section 5, Length).
LENGTH = {"am": (5200, 6900), "pm": (5200, 6900), "eve": (1300, 3500)}   # words: a weekday call is 40 to 50 minutes, a weekend call 10 to 25 (Scott, 13 Nov 2026)
NEVER = [(r"\b((this|my|our|the|a) podcast|(this|today's|yesterday's|tomorrow's|last|next|the|an) episode|the show|my show|our show|"
          r"this show|(this|next|last) segment|(my|dear) listeners?|on air|tune in|tuning in|Morning Briefing|"
          r"answer page|show notes|weekly review|your (scores?|ratings?)|microphone|I'm recording|I record(ed)? this|after I record)\b",
          "she is on the phone with a friend: this is a word from the workshop, not from her world (bible section 0)"),
         (r"\b(Ha|Mm+|Hmph|Heh)\.", "Kokoro drops or misreads this sound"),
         (r"\banswer sheet\b", "there is no answer sheet any more"),
         (r"\b(that's the show|quick hits|lore time|in today's episode|welcome back to)\b", "segment announcement"),
         (r"\b(our date|when we (finally )?meet|meet up (one day|soon|this weekend)|leave (her|your wife)|run away together)\b",
          "she respects his marriage: no plans to meet, nothing that pulls him from his family (bible section 2)")]
MORNING_ONLY = [(r"\bjust (got|came) home from (the shop|work)\b", "morning call: she hasn't been to work yet"),
                (r"\bmy shift today (was|went)\b|\bthe lunch rush today\b", "morning call: today's shift hasn't happened")]
AFTERNOON_ONLY = [(r"\b(last night's|tonight's) raid (was|went)\b.*\btonight\b", "afternoon call: tonight hasn't happened yet")]
REACT = re.compile(r"\[[^\]]*(?:giggl|laugh|chuckl)[^\]]*\]\s*([^.!?\[]{1,60}[.!?])", re.I)


def call_of(name):
    """am, pm or eve for a script file: am_02_..., pm_01_..., eve_03_..., or the fixed names used before 16 Nov 2026."""
    m = re.match(r"^(am|pm|eve)_", name)
    if m:
        return m.group(1)
    if "_evening_" in name:
        return "eve"
    return "am" if name[:2] <= "06" else "pm"


def first_words(path):
    plain = re.sub(r"\[[^\]]*\]", " ", re.sub(r"\{([^|}]*)\|[^}]*\}", r"\1", open(path).read()))
    return " ".join(plain.split()[:6]).lower().strip(" ,.!?…")


def realism(ep, files, d):
    """Guidance, not quotas (bible section 0, Loose, not scripted): FIX only what breaks her world or sounds broken;
    CHECK what usually means she's sounding like a format."""
    import datetime
    print("\n--- Realism check ---")
    words, jokes, laughs, tags, reacts, issues = {}, {}, {}, {}, {}, 0
    for f in files:
        name, raw = os.path.basename(f), open(f).read()
        call = call_of(name)
        plain = re.sub(r"\[[^\]]*\]", " ", re.sub(r"\{([^|}]*)\|[^}]*\}", r"\1", raw))
        words[call] = words.get(call, 0) + len(plain.split())
        for m in re.finditer(r"\[([^\[\]{}]{1,60})\]", raw):
            if tts.kokoro_tags(m.group(0)) == "" and not re.search(r"emphasis|clear|yawn|hum\b", m.group(1), re.I):
                print(f"CHECK {name}: the voice ignores the tag [{m.group(1)}]")
        rules = NEVER + (MORNING_ONLY if call == "am" else AFTERNOON_ONLY if call == "pm" else [])
        for pat, why in rules:
            for m in re.finditer(pat, raw, re.I):
                issues += 1
                print(f"FIX   {name}: \"{m.group(0)}\" ({why})")
        jokes[call] = jokes.get(call, 0) + len(re.findall(r"\[punch\]", raw, re.I))
        laughs[call] = laughs.get(call, 0) + len(re.findall(r"\[[^\]]*(?:giggl|laugh|chuckl)[^\]]*\]", raw, re.I))
        tags[call] = tags.get(call, 0) + len(re.findall(r"\[[^\]]+\]", raw))
        for m in REACT.finditer(raw):
            key = re.sub(r"[^a-z ]", "", m.group(1).lower()).strip()
            reacts[key] = reacts.get(key, 0) + 1
    for call, n in words.items():
        mins = n / 135
        print(f"{call}: {n:,} words, about {mins:.0f} minutes. Jokes with a [punch]: {jokes[call]}. Laugh cues: {laughs[call]}. "
              f"Voice cues: {tags[call]} (one every {n // max(1, tags[call])} words).")
        lo, hi = LENGTH[call]
        if not lo <= n <= hi:
            print(f"CHECK {call}: {n:,} words is outside the usual {lo:,} to {hi:,} (bible section 5, Length).")
        if tags[call] and n / tags[call] < 35:
            print(f"CHECK {call}: a voice cue every {n // tags[call]} words is heavy. Write the speech first and tag only real mood changes (bible section 3).")
        if jokes[call] > 10 or laughs[call] > 8:
            print(f"CHECK {call}: a lot of set-up-and-punch jokes or laugh cues. Does she sound like a person, or a routine?")
    for key, n in sorted(reacts.items(), key=lambda kv: -kv[1]):
        if n > 1:
            issues += 1
            print(f"FIX   the reaction \"{key}\" is used {n} times (each little reaction once a day).")
    # The same hello as a recent call sounds like a show (bible section 5, How a call goes).
    day = datetime.date.fromisoformat(d)
    mine = {call_of(os.path.basename(f)): f for f in sorted(files, reverse=True)}
    firsts = {c: min((f for f in files if call_of(os.path.basename(f)) == c), key=os.path.basename) for c in mine}
    for back in range(1, 6):
        prev = day - datetime.timedelta(days=back)
        for f in glob.glob(f"{tts.REPO}/archive/{prev:%Y/%m}/{prev.isoformat()}/script/*.txt"):
            n = os.path.basename(f)
            if not (re.match(r"^(am|pm|eve)_0*1_", n) or n in ("01_opening_world.txt", "07_walkhome.txt", "01_evening_hello.txt")):
                continue
            old = first_words(f)
            for c, mf in firsts.items():
                if old and first_words(mf) == old:
                    issues += 1
                    print(f"FIX   {os.path.basename(mf)}: starts exactly like the call of {prev.isoformat()} (\"{old}\"). Never the same hello twice running.")
    return issues


def main():
    d = sys.argv[1]
    ep = f"{tts.REPO}/archive/{d[:4]}/{d[5:7]}/{d}"
    files = sorted(glob.glob(f"{ep}/script/*.txt")) + sorted(glob.glob(f"{ep}/headlines/*.txt"))
    half = sys.argv[2] if len(sys.argv) > 2 else ""   # am, pm or eve: which call to check
    if half:
        files = [f for f in files if call_of(os.path.basename(f)) == half]
    if not files:
        print(f"FIX   no script files found for {d} {half or '(whole day)'}: nothing to check.")
        sys.exit(1)
    flagged, scott = 0, 0
    for f in files:
        raw = open(f).read()
        scott += len(re.findall(r"(?<!Ridley )\bScott\b", raw))
        text = re.sub(r"\{[^{}|]*\|[^{}]*\}", " ", raw)  # already settled by hand
        for pat, say in tts.HETERONYMS:
            text = pat.sub(say, text)
        for sent in re.split(r"(?<=[.!?])\s+|\n+", text):
            for m in WORDS.finditer(sent):
                w = m.group(1).lower()
                if w == "used" and not re.search(r"\bused to\b", sent[m.start():], re.I):
                    continue
                flagged += 1
                print(f"{os.path.basename(f)}: \"{w}\" -> {DEFAULTS[w]}\n    {sent.strip()[:200]}")
    issues = realism(ep, [f for f in files if "/script/" in f], d)
    print(f"{issues} thing(s) to FIX." if issues else "Nothing that must be fixed.")
    print(f"\n{flagged} word(s) to check. \"Scott\" used {scott} times in this call "
          f"(where it really lands; a handful a day at most).")


if __name__ == "__main__":
    main()
