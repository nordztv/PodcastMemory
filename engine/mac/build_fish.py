#!/bin/sh
''''exec "$HOME/MorningBriefing/fish/bin/python" "$0" "$@" #'''
"""Morning Briefing on the Mac with Fish Audio S2-Pro (MLX), copying the show's reference voice clip.

Usage: python engine/mac/build_fish.py YYYY-MM-DD [headlines]
Reads archive/YYYY/MM/DATE/script/*.txt (or headlines/*.txt), prepares the text the way the show's rules say
(respellings, pronunciations, capitals as letters, delivery tags), splits it into short chunks (Fish makes at most
about 12 s per call), voices each chunk with the reference clip in engine/mac/voice.json, then joins everything with
pauses between paragraphs and sections, sets the pace and adds chapter markers.
Output: ~/podcast/out/Morning_Briefing_DATE[_headlines].mp3
Finished chunks are kept, so a rerun after an interruption carries on where it stopped.
Set FISH_TEST=1 to voice only the first section and print an estimate for the whole episode.
"""
import glob, inspect, json, os, re, shutil, subprocess, sys, time, wave

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HOME = os.path.expanduser("~")
CFG = json.load(open(f"{REPO}/engine/mac/voice.json"))
# Personal settings that never clash with updates: ~/MorningBriefing/voice.local.json overrides any of the keys above.
LOCAL = f"{HOME}/MorningBriefing/voice.local.json"
if os.path.exists(LOCAL):
    CFG.update({k: v for k, v in json.load(open(LOCAL)).items() if not k.startswith("_")})


def _path(name, ext):
    """A name in engine/mac (ref_happy1), or a full path to your own file (~/Voices/me.wav)."""
    p = os.path.expanduser(name)
    if os.path.isabs(p) or os.path.exists(p):
        return p
    return f"{REPO}/engine/mac/{name}{'' if name.endswith(ext) else ext}"


REF = _path(CFG["ref"], ".wav")
REF_TEXT = open(_path(CFG["ref_text"], ".txt")).read().strip()
CHUNK_WORDS = int(CFG.get("chunk_words", 30))
SR = 24000
PARA_GAP, SECTION_GAP, BEAT = 0.55, 1.8, 0.6
PRONOUNCE = json.load(open(f"{REPO}/show/pronunciations.json"))
HETERONYMS = [(re.compile(p), r) for p, r in json.load(open(f"{REPO}/show/heteronyms.json")) if p != "_comment"]
ROMAN = {"II": "two", "III": "three", "IV": "four", "VI": "six", "VII": "seven", "VIII": "eight", "IX": "nine",
         "XI": "eleven", "XII": "twelve", "XIII": "thirteen", "XIV": "fourteen", "XV": "fifteen", "XVI": "sixteen"}
TAG = re.compile(r"\[(happy|dark|cheeky|serious|normal|beat|punch)\]", re.I)


def prepare(text):
    """The show's text rules, as plain words Fish can read. [beat]/[punch] become a short pause marker."""
    text = text.replace("’", "'").replace("“", '"').replace("”", '"')
    text = re.sub(r"\{[^{}|]*\|([^{}]*)\}", r"\1", text)          # {word|respelling}
    for pat, say in HETERONYMS:
        text = pat.sub(say, text)
    for pat, say in PRONOUNCE.items():
        text = re.sub(pat, say, text, flags=re.I)
    text = re.sub(r"\[(beat|punch)\]", " ‖ ", text, flags=re.I)  # pause marker, split on below
    text = TAG.sub("", text)
    text = re.sub(r"\b(II|III|IV|VI|VII|VIII|IX|XI|XII|XIII|XIV|XV|XVI)\b", lambda m: ROMAN[m.group(1)], text)
    text = re.sub(r"\b([A-Z]{2,6})('?s)?\b", lambda m: " ".join(m.group(1)) + ("s" if m.group(2) else ""), text)
    return text


def pieces(text):
    """Yields ("say", text) chunks of whole sentences, ("beat", None) and ("para", None) markers."""
    for para in [p.strip() for p in prepare(text).split("\n") if p.strip()]:
        for part in para.split("‖"):
            cur = []
            sents = []
            for s in [s for s in re.split(r"(?<=[.!?])\s+", part.strip()) if s.strip()]:
                # a very long sentence is split at commas, colons or semicolons, so no call runs past Fish's limit
                sents += re.split(r"(?<=[,;:])\s+", s) if len(s.split()) > CHUNK_WORDS * 1.3 else [s]
            for s in sents:
                if cur and len(" ".join(cur + [s]).split()) > CHUNK_WORDS:
                    yield "say", " ".join(cur); cur = []
                cur.append(s)
            if cur:
                yield "say", " ".join(cur)
            yield "beat", None
        yield "para", None


def load():
    from mlx_audio.tts.utils import load_model
    last = None
    for mid in CFG["models"]:
        try:
            print(f"Loading {mid}", flush=True)
            return load_model(mid), mid
        except Exception as e:  # try the next model id
            print(f"  could not load {mid}: {e}", flush=True); last = e
    raise SystemExit(f"No Fish model could be loaded: {last}")


def voice(model, text, dest, tmp):
    from mlx_audio.tts.generate import generate_audio
    shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    want = dict(model=model, text=text, ref_audio=REF, ref_text=REF_TEXT, output_path=tmp, file_prefix="c",
                join_audio=True, audio_format="wav", verbose=False, play=False)
    accepted = inspect.signature(generate_audio).parameters
    takes_all = any(p.kind == p.VAR_KEYWORD for p in accepted.values())
    args = {k: v for k, v in want.items() if takes_all or k in accepted}
    cwd = os.getcwd(); os.chdir(tmp)   # older versions write to the current folder
    try:
        generate_audio(**args)
    finally:
        os.chdir(cwd)
    wavs = sorted(glob.glob(f"{tmp}/**/*.wav", recursive=True), key=os.path.getmtime)
    if not wavs:
        return False
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wavs[-1], "-ar", str(SR), "-ac", "1", dest], check=True)
    return True


def secs(path):
    w = wave.open(path); return w.getnframes() / w.getframerate()


def main():
    d = sys.argv[1]
    headlines = len(sys.argv) > 2 and sys.argv[2] == "headlines"
    src = f"{REPO}/archive/{d[:4]}/{d[5:7]}/{d}/" + ("headlines" if headlines else "script")
    work = f"{HOME}/podcast/render_fish/{d}" + ("_headlines" if headlines else ""); out = f"{HOME}/podcast/out"
    os.makedirs(work, exist_ok=True); os.makedirs(out, exist_ok=True)
    for name, s in (("pgap", PARA_GAP), ("sgap", SECTION_GAP), ("beat", BEAT)):
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono", "-t", str(s), f"{work}/{name}.wav"], check=True)
    files = sorted(glob.glob(f"{src}/*.txt"))
    if not files:
        raise SystemExit(f"No script in {src}")
    if os.environ.get("FISH_TEST"):
        files = files[:1]
    model, mid = load()
    order, timings, failed, words, speech, start = [], [], 0, 0, 0.0, time.time()
    for f in files:
        sec = os.path.basename(f)[:-4]; first = len(order); n = 0
        for kind, text in pieces(open(f).read()):
            if kind == "beat":
                if len(order) > first and not order[-1].endswith(("beat.wav", "pgap.wav")):
                    order.append(f"{work}/beat.wav")
                continue
            if kind == "para":
                if order and order[-1].endswith("beat.wav"):
                    order[-1] = f"{work}/pgap.wav"
                else:
                    order.append(f"{work}/pgap.wav")
                continue
            dest = f"{work}/{sec}_{n:04d}.wav"; n += 1
            if not os.path.exists(dest):
                try:
                    ok = voice(model, text, dest, f"{work}/tmp")
                except Exception as e:
                    print(f"  error: {e}", flush=True); ok = False
                if not ok:
                    print(f"FAILED: {sec} chunk {n}", flush=True); failed += 1; continue
            order.append(dest); words += len(text.split()); speech += secs(dest)
        if len(order) > first:
            order[-1:] = [f"{work}/sgap.wav"]
            timings.append((sec, sum(secs(p) for p in order[first:])))
        print(f"{sec} done, {int(time.time() - start)}s so far", flush=True)
        if failed > 10:
            raise SystemExit("Too many chunks failed; stopping")
    target = CFG.get("words_per_minute")
    tempo = max(0.8, min(1.0, target / (words / speech * 60))) if target and speech else 1.0
    print(f"Pace: {words / max(speech, 1) * 60:.0f} words a minute; tempo {tempo:.2f}", flush=True)
    with open(f"{work}/list.txt", "w") as lst:
        lst.writelines(f"file '{p}'\n" for p in order)
    mp3 = f"{out}/Morning_Briefing_{d}" + ("_headlines" if headlines else "") + ".mp3"
    af = ([f"atempo={tempo:.3f}"] if tempo < 0.99 else []) + ["loudnorm=I=-16:TP=-1.5:LRA=11"]
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{work}/list.txt", "-af", ",".join(af),
                    "-ar", str(SR), "-ac", "1", "-b:a", "128k", "-metadata", f"title=Morning Briefing - {d}",
                    "-metadata", "artist=Morning Briefing", mp3], check=True)
    with open(f"{work}/timings.txt", "w") as t:
        t.writelines(f"{s}\t{v / tempo}\n" for s, v in timings)
    if subprocess.run([sys.executable, f"{REPO}/engine/chapters.py", mp3, f"{work}/timings.txt", d] + (["headlines"] if headlines else [])).returncode:
        print("chapters skipped (episode is fine without them)", flush=True)
    took = time.time() - start
    print(f"Done: {mp3} with {mid} ({failed} chunks failed), {int(took)}s", flush=True)
    if os.environ.get("FISH_TEST"):
        all_words = sum(len(open(f).read().split()) for f in sorted(glob.glob(f"{src}/*.txt")))
        test_words = len(open(files[0]).read().split())
        print(f"SPEED TEST: {test_words} words took {took / 60:.1f} min. The full episode ({all_words} words) "
              f"would take about {took * all_words / test_words / 60:.0f} min on this Mac.", flush=True)
    sys.exit(1 if failed > 3 else 0)


if __name__ == "__main__":
    main()
