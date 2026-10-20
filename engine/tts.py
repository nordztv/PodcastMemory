"""Morning Briefing text-to-speech: one plain-text script file -> one MP3.

Usage: python3 engine/tts.py script.txt out.mp3 [voice] [speed]
Defaults to the show voice "Happy 1" (af_heart:0.5+af_bella:0.3+af_nicole:0.2) at speed 0.92.
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
SR = 24000
PUNCT = ",.!?;:—"
SHOW_VOICE = "af_heart:0.5+af_bella:0.3+af_nicole:0.2"  # "Happy 1", chosen 19 Oct 2026
SHOW_SPEED = 0.92


SYSTEM_ESPEAK = os.environ.get("ESPEAK_NG")  # e.g. Homebrew's espeak-ng on a Mac; default is the bundled Linux copy


def espeak(text):
    if SYSTEM_ESPEAK:
        cmd, env = [SYSTEM_ESPEAK, "-q", "--ipa=3", "-v", "en-us", text], None
    else:
        cmd, env = [f"{PIPER}/espeak-ng", f"--path={PIPER}", "-q", "--ipa=3", "-v", "en-us", text], {"LD_LIBRARY_PATH": PIPER}
    out = subprocess.run(cmd, capture_output=True, text=True, env=env).stdout
    return " ".join(out.split())


def phonemize(sentence):
    ph = ""
    for p in re.split(r"([,.!?;:—])", sentence):
        if not p.strip():
            continue
        if p in PUNCT:
            ph = ph.rstrip() + ("," if p == "—" else p) + " "
        else:
            ph += espeak(p) + " "
    return "".join(c for c in ph.strip() if c in VOCAB)


# Delivery cues the script can use (bible section 3, Delivery cues). Mood tags apply from where they appear to the
# end of that paragraph; each new paragraph starts back at "normal".
#   voice blend, speed (tempo), pitch (x1.0 = unchanged), gain, pause after each sentence (s)
MOODS = {
    "normal":  dict(voice=None, speed=None, pitch=1.00, gain=1.00, gap=0.18),
    "happy":   dict(voice="af_heart:0.4+af_bella:0.5+af_nicole:0.1", speed=1.00, pitch=1.035, gain=1.06, gap=0.15),
    "dark":    dict(voice="af_heart:0.45+af_nicole:0.55", speed=0.82, pitch=0.94, gain=0.88, gap=0.40),
    "serious": dict(voice="af_heart:0.7+af_nicole:0.3", speed=0.87, pitch=0.98, gain=0.95, gap=0.28),
}
BEAT, PUNCH_BEAT, PUNCH_SLOW, PUNCH_GAIN, PARA_GAP = 0.7, 0.55, 0.9, 1.15, 0.55
TAG = re.compile(r"\[(happy|dark|serious|normal|beat|punch)\]", re.I)


def sentences(text):
    """Yields (kind, value, mood, punch): kind is "say" (value = sentence), "pause" (value = seconds) or "para"."""
    text = text.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    for pat, say in PRONOUNCE.items():
        text = re.sub(pat, say, text, flags=re.I)
    for para in [p.strip() for p in text.split("\n") if p.strip()]:
        mood, punch = "normal", False
        for part in TAG.split(para):
            low = part.lower()
            if low in MOODS:
                mood = low
            elif low == "beat":
                yield "pause", BEAT, mood, False
            elif low == "punch":
                punch = True
            else:
                for s in re.split(r"(?<=[.!?])\s+", part.strip()):
                    if s.strip():
                        if punch:
                            yield "pause", PUNCH_BEAT, mood, False
                        yield "say", s, mood, punch
                        punch = False
        yield "para", PARA_GAP, "normal", False


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
    chunks = []
    for kind, val, mood, punch in sentences(open(src).read()):
        if kind != "say":
            chunks.append(np.zeros(int(SR * val), np.float32))
            continue
        ph = phonemize(val)
        if not ph:
            continue
        cfg = MOODS[mood]
        tempo = (cfg["speed"] or speed) * (PUNCH_SLOW if punch else 1)
        ids = [VOCAB[c] for c in ph][:510]
        audio = sess.run(None, {tok_name: np.array([[0, *ids, 0]], np.int64),
                                "style": styles[mood][len(ids) - 1].astype(np.float32),
                                "speed": np.array([tempo / cfg["pitch"]], np.float32)})[0].ravel()
        audio = shift_pitch(audio, cfg["pitch"]) * cfg["gain"] * (PUNCH_GAIN if punch else 1)
        chunks += [audio, np.zeros(int(SR * (cfg["gap"] + (0.25 if punch else 0))), np.float32)]
    wav = np.concatenate(chunks)
    pcm = (np.clip(wav, -1, 1) * 32767).astype(np.int16).tobytes()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-",
                    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-b:a", "128k", out], input=pcm, check=True)
    print(f"{out}: {len(wav) / SR:.1f}s")


if __name__ == "__main__":
    main()
