"""Morning Briefing text-to-speech: one plain-text script file -> one MP3.

Usage: python3 engine/tts.py script.txt out.mp3 [voice] [speed]
Defaults to the show voice (af_heart:0.7+af_nicole:0.3) at speed 0.92.
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
SHOW_VOICE = "af_heart:0.7+af_nicole:0.3"
SHOW_SPEED = 0.92


def espeak(text):
    out = subprocess.run([f"{PIPER}/espeak-ng", f"--path={PIPER}", "-q", "--ipa=3", "-v", "en-us", text],
                         capture_output=True, text=True, env={"LD_LIBRARY_PATH": PIPER}).stdout
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


def sentences(text):
    text = text.replace("’", "'").replace("“", '"').replace("”", '"')
    for pat, say in PRONOUNCE.items():
        text = re.sub(pat, say, text, flags=re.I)
    for para in [p.strip() for p in text.split("\n") if p.strip()]:
        for s in re.split(r"(?<=[.!?])\s+", para):
            yield s, False
        yield None, True


def main():
    src, out = sys.argv[1], sys.argv[2]
    voice = sys.argv[3] if len(sys.argv) > 3 else SHOW_VOICE
    speed = float(sys.argv[4]) if len(sys.argv) > 4 else SHOW_SPEED
    sess = rt.InferenceSession(MODEL, providers=["CPUExecutionProvider"])
    names = {i.name for i in sess.get_inputs()}
    tok_name = "input_ids" if "input_ids" in names else "tokens"
    bank = np.load(VOICES)
    vstyle = sum(float(w) * bank[n] for n, w in (p.split(":") if ":" in p else (p, 1) for p in voice.split("+")))
    chunks = []
    for s, brk in sentences(open(src).read()):
        if brk:
            chunks.append(np.zeros(int(SR * 0.55), np.float32))
            continue
        ph = phonemize(s)
        if not ph:
            continue
        ids = [VOCAB[c] for c in ph][:510]
        audio = sess.run(None, {tok_name: np.array([[0, *ids, 0]], np.int64),
                                "style": vstyle[len(ids) - 1].astype(np.float32),
                                "speed": np.array([speed], np.float32)})[0].ravel()
        chunks += [audio, np.zeros(int(SR * 0.18), np.float32)]
    wav = np.concatenate(chunks)
    pcm = (np.clip(wav, -1, 1) * 32767).astype(np.int16).tobytes()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-",
                    "-af", "loudnorm=I=-16:TP=-1.5", "-b:a", "128k", out], input=pcm, check=True)
    print(f"{out}: {len(wav) / SR:.1f}s")


if __name__ == "__main__":
    main()
