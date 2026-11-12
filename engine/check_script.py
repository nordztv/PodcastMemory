"""Pre-recording check of an episode's script: words the voice engine could say the wrong way, and name overuse.

Usage: python3 engine/check_script.py YYYY-MM-DD
For every word that's spelled the same but said two ways (live, read, close...) and that show/heteronyms.json didn't
already settle from context, prints the sentence and what the engine will say by default. If that's the wrong one,
write {word|respelling} in the script (for example {live|lyve}, {read|red}, {close|kloze}). Also counts "Scott".

Then a realism check (bible sections 2, 3 and 5): the exact opening line, words per part against the budget, tags
the voice engine would silently drop, how often she jokes and whether her little reactions repeat, whispered
secrets, phrases that break the two-call time model, and words that must never be said. "CHECK" lines need a look;
"FIX" lines must be fixed before committing.
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


OPENING = "Ohayou gozaimasu, Scott. I hope you are doing well today."
BUDGET = {"01": 700, "02": 1200, "03": 1400, "04": 1800, "05": 1400, "06": 1100, "07": 450, "08": 800, "09": 800,
          "10": 400, "11": 900}
NEVER = [(r"\bX-?M5\b", "the X-M5 is never mentioned"), (r"\byour wife\b", "never mention his wife"),
         (r"\b(Ha|Mm+|Hmph|Heh)\.", "Kokoro drops or misreads this sound"),
         (r"\banswer sheet\b", "there is no answer sheet any more"),
         (r"\b(that's the show|quick hits|lore time|in today's episode|welcome back to)\b", "segment announcement"),
         (r"\[(ominous|eerie|low voice|screaming|shouting|singing|moaning)", "banned delivery tag"),
         (r"\bI love you\b|\bour date\b", "sounds like a romance")]
MORNING_ONLY = [(r"\bjust (got|came) home from (the shop|work)\b", "morning call: she hasn't been to work yet"),
                (r"\bmy shift today (was|went)\b|\bthe lunch rush today\b", "morning call: today's shift hasn't happened"),
                (r"\bthis morning's news\b|\boverni?ght,? (the|a|an) \w+ (said|announced)", "she only knows news up to the evening before")]
AFTERNOON_ONLY = [(r"\b(last night's|tonight's) raid (was|went)\b.*\btonight\b", "afternoon call: tonight hasn't happened yet")]
REACT = re.compile(r"\[[^\]]*(?:giggl|laugh|chuckl)[^\]]*\]\s*([^.!?\[]{1,60}[.!?])", re.I)


def realism(ep, files, weekday):
    print("\n--- Realism check ---")
    budget = dict(BUDGET)
    if weekday == 4:
        budget.update({"11": 1800, "08": 650, "09": 650})
    total, jokes, laughs, whispers, spooky, reacts, issues = 0, 0, 0, 0, 0, {}, 0
    for f in files:
        name, raw = os.path.basename(f), open(f).read()
        plain = re.sub(r"\[[^\]]*\]", " ", re.sub(r"\{([^|}]*)\|[^}]*\}", r"\1", raw))
        words = len(plain.split())
        total += words
        want = budget.get(name[:2])
        if want and not 0.7 * want <= words <= 1.35 * want:
            print(f"CHECK {name}: {words} words (budget about {want})")
        if name.startswith("01") and not raw.lstrip().startswith(OPENING):
            issues += 1
            print(f"FIX   {name}: must begin exactly: {OPENING}")
        for m in re.finditer(r"\[([^\[\]{}]{1,60})\]", raw):
            if tts.kokoro_tags(m.group(0)) == "" and not re.search(r"emphasis|clear|yawn|hum\b", m.group(1), re.I):
                print(f"CHECK {name}: the voice ignores the tag [{m.group(1)}]")
        rules = NEVER + (MORNING_ONLY if name[:2] <= "06" else AFTERNOON_ONLY)
        for pat, why in rules:
            for m in re.finditer(pat, raw, re.I):
                issues += 1
                print(f"FIX   {name}: \"{m.group(0)}\" ({why})")
        if name[:2] != "11" or weekday != 4:
            for m in re.finditer(r"\byour (son|little one|boy)\b", raw, re.I):
                issues += 1
                print(f"FIX   {name}: \"{m.group(0)}\" (his son is only mentioned in Friday's weekend ideas)")
        jokes += len(re.findall(r"\[punch\]", raw, re.I))
        laughs += len(re.findall(r"\[[^\]]*(?:giggl|laugh|chuckl)[^\]]*\]", raw, re.I))
        whispers += len(re.findall(r"\[[^\]]*(?:secretive|whisper|hushed)[^\]]*\]\s*Okay", raw, re.I))
        spooky += 1 if re.search(r"\[sweet, innocent\]", raw, re.I) else 0
        for m in REACT.finditer(raw):
            key = re.sub(r"[^a-z ]", "", m.group(1).lower()).strip()
            reacts[key] = reacts.get(key, 0) + 1
    print(f"Words: {total:,} (target 10,000 to 11,000).")
    print(f"Jokes with a [punch]: {jokes} (bible section 3: about 12 to 18 an episode, never the same shape twice in a row).")
    print(f"Laugh tags: {laughs} (at most about half the jokes; a laugh she doesn't need is the one to cut).")
    if jokes > 20 or laughs > 14:
        print("CHECK too many jokes or laughs: it starts to sound like a routine instead of a person.")
    for key, n in sorted(reacts.items(), key=lambda kv: -kv[1]):
        if n > 1:
            issues += 1
            print(f"FIX   the reaction \"{key}\" is used {n} times (each little reaction once an episode).")
    apologies = sum(n for k, n in reacts.items() if k.startswith("sorry") or k.startswith("okay"))
    if apologies > 3:
        print(f"CHECK {apologies} reactions start with 'Sorry' or 'Okay': vary them.")
    print(f"Whispered secrets: {whispers} (one to three, outside the news). Sweet-spooky moments: {spooky}.")
    if whispers == 0:
        print("CHECK no whispered secret in this episode.")
    return issues


def main():
    d = sys.argv[1]
    ep = f"{tts.REPO}/archive/{d[:4]}/{d[5:7]}/{d}"
    files = sorted(glob.glob(f"{ep}/script/*.txt")) + sorted(glob.glob(f"{ep}/headlines/*.txt"))
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
    import datetime
    issues = realism(ep, [f for f in files if "/script/" in f], datetime.date.fromisoformat(d).weekday())
    print(f"{issues} thing(s) to FIX." if issues else "Nothing that must be fixed.")
    print(f"\n{flagged} word(s) to check. \"Scott\" used {scott} times across the episode "
          f"(rule: greeting, maybe the goodbye, and at most two or three others).")


if __name__ == "__main__":
    main()
