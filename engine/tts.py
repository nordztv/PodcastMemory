"""Morning Briefing text-to-speech: one plain-text script file -> one MP3.

Usage: python3 engine/tts.py script.txt out.mp3 [voice] [speed]
Defaults to the show voice "Happy 1" (af_heart:0.5+af_bella:0.3+af_nicole:0.2) at speed 0.92.
Renders paragraph-sized chunks (sentences of the same mood together, up to 400 phonemes) rather than one sentence
at a time, so intonation carries across sentences (2 Nov 2026).
Pronunciation fixes live in show/pronunciations.json (regex -> how to say it).
Voice files are installed by engine/setup.sh.
"""
import json, os, re, subprocess, sys
import numpy as np
import onnxruntime as rt

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = os.path.expanduser("~")
PIPER = f"{HOME}/dl/piper/piper"
MODEL = f"{HOME}/tts/kokoro-v1.0.onnx"
VOICES = f"{HOME}/tts/voices-v1.0.bin"
VOCAB = json.load(open(f"{REPO}/engine/kokoro_config.json"))["vocab"]
PRONOUNCE = json.load(open(f"{REPO}/show/pronunciations.json"))
HETERONYMS = [(re.compile(p), r) for p, r in json.load(open(f"{REPO}/show/heteronyms.json")) if p != "_comment"]
# Letter names as phonemes, so capitals are always spelled out the same way (AMD -> A M D, never "uh M D").
LETTERS = {"A": "ˈeɪ", "B": "bˈiː", "C": "sˈiː", "D": "dˈiː", "E": "ˈiː", "F": "ˈɛf", "G": "dʒˈiː", "H": "ˈeɪtʃ",
           "I": "ˈaɪ", "J": "dʒˈeɪ", "K": "kˈeɪ", "L": "ˈɛl", "M": "ˈɛm", "N": "ˈɛn", "O": "ˈoʊ", "P": "pˈiː",
           "Q": "kjˈuː", "R": "ˈɑːɹ", "S": "ˈɛs", "T": "tˈiː", "U": "jˈuː", "V": "vˈiː", "W": "dˈʌbəljuː",
           "X": "ˈɛks", "Y": "wˈaɪ", "Z": "zˈɛd"}
ROMAN = {"II": "two", "III": "three", "IV": "four", "VI": "six", "VII": "seven", "VIII": "eight", "IX": "nine",
         "XI": "eleven", "XII": "twelve", "XIII": "thirteen", "XIV": "fourteen", "XV": "fifteen", "XVI": "sixteen"}


def spell(letters, plural=""):
    """Phonemes for a run of capital letters, wrapped in «» so phonemize passes them straight through."""
    ph = " ".join(LETTERS[c] for c in letters)
    return f"«{ph}{'z' if plural else ''}»"


def say_capitals(text):
    """Capitalised words are said as letters: AMD, A S M L, GPUs. Words like NASA are listed in pronunciations.json."""
    def spaced(m):
        t = m.group(0)
        return spell(re.sub(r"'?s$", "", t).replace(" ", ""), "s" if re.search(r"'?s$", t) else "")
    text = re.sub(r"\b(?:[A-Z] ){1,7}[A-Z](?:'?s)?\b", spaced, text)
    text = re.sub(r"\b(II|III|IV|VI|VII|VIII|IX|XI|XII|XIII|XIV|XV|XVI)\b", lambda m: ROMAN[m.group(1)], text)
    return re.sub(r"\b([A-Z]{2,6})('?s)?\b", lambda m: spell(m.group(1), m.group(2)), text)
SR = 24000
PUNCT = ",.!?;:—…"
SHOW_VOICE = "af_heart:0.5+af_bella:0.3+af_nicole:0.2"  # "Happy 1", chosen 19 Oct 2026
SHOW_SPEED = 0.92


SYSTEM_ESPEAK = os.environ.get("ESPEAK_NG")  # e.g. Homebrew's espeak-ng on a Mac; default is the bundled Linux copy


def espeak(text):
    # A segment that starts with "-" (e.g. "GPU-hunter" after the capitals are spelled out) would be read by
    # espeak-ng as a command-line option, and its help text would then be spoken as gibberish (2 Nov 2026 bug).
    text = text.strip().lstrip("-–").strip()
    if not text:
        return ""
    if SYSTEM_ESPEAK:
        cmd, env = [SYSTEM_ESPEAK, "-q", "--ipa=3", "-v", "en-us", text], None
    else:
        cmd, env = [f"{PIPER}/espeak-ng", f"--path={PIPER}", "-q", "--ipa=3", "-v", "en-us", text], {"LD_LIBRARY_PATH": PIPER}
    out = subprocess.run(cmd, capture_output=True, text=True, env=env).stdout
    if "espeak-ng [options]" in out or "text-to-speech:" in out:   # never speak a usage message
        return ""
    return " ".join(out.split())


def phonemize(sentence):
    ph = ""
    for i, chunk in enumerate(re.split(r"«([^»]*)»", sentence)):
        if i % 2:  # already phonemes (spelled-out letters)
            ph += chunk + " "
            continue
        ph += phonemize_text(chunk) + " "
    return "".join(c for c in " ".join(ph.split()) if c in VOCAB)


def phonemize_text(sentence):
    ph = ""
    sentence = re.sub(r"\.\.\.|…", " … ", sentence)  # an ellipsis is a hesitation, not three full stops
    for p in re.split(r"([,.!?;:—…])", sentence):
        if not p.strip():
            continue
        if p in PUNCT:
            ph = ph.rstrip() + ("," if p == "—" else p) + " "
        else:
            ph += espeak(p) + " "
    return "".join(c for c in ph.strip() if c in VOCAB)


# Delivery cues the script can use (bible section 3, Delivery cues). Mood tags apply from where they appear to the
# end of that paragraph; each new paragraph starts back at "normal".
# Kokoro has no emotion input: a mood is a voice blend plus small tempo, volume and pause changes. Pitch is kept
# within 2% (it's done by resampling, which changes the character of the voice if pushed further).
#   voice blend, speed (tempo), pitch (x1.0 = unchanged), gain, pause after each chunk (s)
MOODS = {
    "normal":  dict(voice=None, speed=None, pitch=1.00, gain=1.00, gap=0.22),
    "happy":   dict(voice="af_heart:0.4+af_bella:0.5+af_nicole:0.1", speed=0.97, pitch=1.015, gain=1.05, gap=0.18),
    "cheeky":  dict(voice="af_heart:0.5+af_bella:0.4+af_nicole:0.1", speed=0.90, pitch=1.01, gain=1.02, gap=0.30),
    "serious": dict(voice="af_heart:0.7+af_nicole:0.3", speed=0.88, pitch=0.99, gain=0.96, gap=0.28),
    "dark":    dict(voice="af_heart:0.45+af_nicole:0.55", speed=0.83, pitch=1.00, gain=0.88, gap=0.40),
    # whispered secrets: af_nicole is Kokoro's breathiest voice; quieter, slower, longer gaps (not a true whisper)
    "whisper": dict(voice="af_heart:0.3+af_nicole:0.7", speed=0.84, pitch=1.00, gain=0.74, gap=0.45),
}
MOOD_NAMES = "|".join(MOODS)
PAUSES = {"beat": 0.6, "shortbeat": 0.35, "longbeat": 1.2, "pause": 0.4, "shortpause": 0.25,
          "laughgap": 0.25, "sighgap": 0.35}   # the last two stand in for sounds Kokoro can't make
PUNCH_SLOW, PUNCH_GAIN, PARA_GAP = 0.92, 1.12, 0.55
MAX_PH = 400        # phonemes per Kokoro call (the model's hard limit is 510)
# Transitions: each chunk moves this far from the current tone towards the new one (1.0 = instant).
EASE = 0.75
TAG = re.compile(r"\[(" + MOOD_NAMES + r"|punch|" + "|".join(PAUSES) + r")\]", re.I)
# Spoken-sound filler written after a sound tag ("Ha.", "Mm.", "Hmph."): Kokoro would read it as a word, so it's dropped.
FILLER = re.compile(r"^(ha+|ha ha|mm+|hmm*|hmph|heh)[.!,]*$", re.I)


# Scripts use free-form delivery tags ([excited], [teasing tone], [giggling while talking]...). Kokoro only knows the
# moods above, so each tag maps to the nearest one (first match wins); laughs and sighs become short pauses.
KOKORO_MAP = [
    (r"short beat", "[shortbeat]"), (r"long beat", "[longbeat]"), (r"short pause", "[shortpause]"),
    (r"^pause$|^break$", "[pause]"), (r"beat", "[beat]"),
    (r"punch", "[punch]"),
    (r"laugh|chuckl|giggl|snicker", "[laughgap]"),
    (r"sigh|huff|exhale|inhale|breath|gasp|groan|tsk|scoff", "[sighgap]"),
    (r"emphasis|clear|yawn|hum\b", ""),
    (r"whisper|hushed|secretive|very quiet", "[whisper]"),
    (r"sweet|innocent|dark|low voice|menac|eerie|creep|ominous|sinister|deadpan|matter-of-fact", "[dark]"),
    (r"tease|teasing|cheeky|playful|flirt|wink|sarcas|smirk|amused|mischiev|sly|knowing|smug|mock|dry", "[cheeky]"),
    (r"sad|serious|calm|sombre|somber|grave|sympath|compassion|empath|gentle|moved|respect|professional|"
     r"disappoint|frustrat|exasperat|soft", "[serious]"),
    (r"happy|excit|delight|cheer|joy|bright|enthus|thrill|proud|grateful|optimis|warm|impressed|relieved|upbeat|"
     r"encourag|energ", "[happy]"),
    (r"curious|thoughtful|dreamy|nostalg|surprise|interest|relax|friendly|neutral", "[normal]"),
]


def kokoro_tags(text):
    def one(m):
        inner = m.group(1).lower().strip()
        if re.fullmatch(MOOD_NAMES + "|punch|" + "|".join(PAUSES), inner):
            return m.group(0)
        for pat, rep in KOKORO_MAP:
            if re.search(pat, inner):
                return rep
        return ""
    text = re.sub(r"\[([^\[\]{}]{1,60})\]", one, text)
    moods = r"\[(?:" + MOOD_NAMES + r")\]"
    return re.sub(r"(" + moods + r")(\s*" + moods + r")+", r"\1", text)   # stacked moods: the first one wins


def sentences(text):
    """Yields (kind, value, mood, punch): kind is "say" (value = sentence), "pause" (value = seconds) or "para"."""
    text = text.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    text = kokoro_tags(text)
    text = re.sub(r"\{[^{}|]*\|([^{}]*)\}", r"\1", text)  # {word|how to say it}, written into the script
    for pat, say in HETERONYMS:
        text = pat.sub(say, text)
    for pat, say in PRONOUNCE.items():
        text = re.sub(pat, say, text, flags=re.I)
    for para in [p.strip() for p in text.split("\n") if p.strip()]:
        mood, punch = "normal", False
        for part in TAG.split(para):
            low = part.lower()
            if low in MOODS:
                mood = low
            elif low in PAUSES:
                yield "pause", PAUSES[low], mood, False
            elif low == "punch":
                punch = True
            else:
                for s in re.split(r"(?<=[.!?])\s+", say_capitals(part.strip())):
                    if s.strip() and not FILLER.match(s.strip()):
                        if punch:
                            yield "pause", PAUSES["beat"], mood, False
                        yield "say", s, mood, punch
                        punch = False
        yield "para", PARA_GAP, "normal", False


def chunks_of(events):
    """Joins consecutive sentences of the same mood into one chunk of up to MAX_PH phonemes, so Kokoro plans the
    phrasing across them (one sentence per call made every line end like the end of a speech). A punch line, a
    pause, a mood change or a new paragraph starts a new chunk."""
    buf, buf_ph, buf_mood = [], [], None
    def flush():
        if buf:
            yield "say", " ".join(buf_ph), buf_mood, False
        buf.clear(); buf_ph.clear()
    for kind, val, mood, punch in events:
        if kind != "say":
            yield from flush()
            yield kind, val, mood, punch
            continue
        ph = phonemize(val)
        if not ph:
            continue
        if punch:
            yield from flush()
            yield "say", ph, mood, True
            continue
        if buf and (mood != buf_mood or len(" ".join(buf_ph + [ph])) > MAX_PH):
            yield from flush()
        buf.append(val); buf_ph.append(ph); buf_mood = mood
    yield from flush()


def shift_pitch(audio, factor):
    """Raises (factor > 1) or lowers the pitch by resampling; the caller pre-adjusts speed so the tempo is right."""
    if abs(factor - 1) < 0.005:
        return audio
    n = len(audio)
    return np.interp(np.arange(0, n - 1, factor), np.arange(n), audio).astype(np.float32)


def main():
    src, out = sys.argv[1], sys.argv[2]
    voice = sys.argv[3] if len(sys.argv) > 3 else SHOW_VOICE
    speed = float(sys.argv[4]) if len(sys.argv) > 4 else SHOW_SPEED
    sess = rt.InferenceSession(MODEL, providers=["CPUExecutionProvider"])
    names = {i.name for i in sess.get_inputs()}
    tok_name = "input_ids" if "input_ids" in names else "tokens"
    bank = np.load(VOICES)
    blend = lambda v: sum(float(w) * bank[n] for n, w in (p.split(":") if ":" in p else (p, 1) for p in v.split("+")))
    styles = {m: blend(cfg["voice"] or voice) for m, cfg in MOODS.items()}
    weights = {m: float(m == "normal") for m in MOODS}   # how much of each tone is in her voice right now
    mix = lambda key, default=None: sum(w * (MOODS[m][key] or default) for m, w in weights.items())
    chunks = []
    for kind, ph, mood, punch in chunks_of(sentences(open(src).read())):
        if kind != "say":
            chunks.append(np.zeros(int(SR * ph), np.float32))
            continue
        weights = {m: w + ((m == mood) - w) * EASE for m, w in weights.items()}
        pitch, gain, gap = mix("pitch"), mix("gain"), mix("gap")
        tempo = mix("speed", speed) * (PUNCH_SLOW if punch else 1)
        ids = [VOCAB[c] for c in ph][:510]
        style = sum(w * styles[m][len(ids) - 1] for m, w in weights.items() if w > 1e-3)
        audio = sess.run(None, {tok_name: np.array([[0, *ids, 0]], np.int64),
                                "style": style.astype(np.float32),
                                "speed": np.array([tempo / pitch], np.float32)})[0].ravel()
        audio = shift_pitch(audio, pitch) * gain * (PUNCH_GAIN if punch else 1)
        chunks += [audio, np.zeros(int(SR * (gap + (0.2 if punch else 0))), np.float32)]
    wav = np.concatenate(chunks)
    pcm = (np.clip(wav, -1, 1) * 32767).astype(np.int16).tobytes()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-",
                    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-b:a", "128k", out], input=pcm, check=True)
    print(f"{out}: {len(wav) / SR:.1f}s")


if __name__ == "__main__":
    main()
