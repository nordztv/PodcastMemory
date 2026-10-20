"""Pre-recording check of an episode's script: words the voice engine could say the wrong way, and name overuse.

Usage: python3 engine/check_script.py YYYY-MM-DD
For every word that's spelled the same but said two ways (live, read, close...) and that show/heteronyms.json didn't
already settle from context, prints the sentence and what the engine will say by default. If that's the wrong one,
write {word|respelling} in the script (for example {live|lyve}, {read|red}, {close|kloze}). Also counts "Scott".
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
    print(f"\n{flagged} word(s) to check. \"Scott\" used {scott} times across the episode "
          f"(rule: greeting, maybe the goodbye, and at most two or three others).")


if __name__ == "__main__":
    main()
