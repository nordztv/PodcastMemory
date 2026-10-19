"""Morning Briefing on the Mac with VoxCPM2 (Scott's chosen voice, cloned from the show's Heart clip).

Usage: python3 engine/mac/build_voxcpm.py YYYY-MM-DD
Reads archive/YYYY/MM/DATE/script/*.txt, applies show/pronunciations.json, splits the text into chunks of a
few paragraphs, voices each chunk with mlx-audio (VoxCPM2), then joins everything with short pauses between
paragraphs and longer ones between sections. Output: ~/podcast/out/Morning_Briefing_DATE.mp3 (128 kbps).
Already-made chunks are kept, so a rerun after an interruption carries on where it stopped.
"""
import glob, json, os, re, shutil, subprocess, sys, time

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HOME = os.path.expanduser("~")
GEN = f"{HOME}/MorningBriefing/mlx/bin/mlx_audio.tts.generate"
MODEL = os.environ.get("VOX_MODEL", "mlx-community/VoxCPM2-8bit")
# The voice is set by engine/mac/voice.json: which reference clip VoxCPM2 copies, and whether to add the soft finish.
CFG = json.load(open(f"{REPO}/engine/mac/voice.json"))
REF = f"{REPO}/engine/mac/{CFG['ref']}.wav"
REF_TEXT = open(f"{REPO}/engine/mac/{CFG['ref_text']}.txt").read().strip()
SOFT = "lowshelf=f=220:g=1.5,equalizer=f=3500:t=q:w=1.2:g=-3,highshelf=f=7000:g=-4,deesser,acompressor=threshold=-22dB:ratio=2.5:attack=15:release=200"
CHUNK_WORDS = 120          # small chunks keep a cloned voice steady over a long episode
PARA_GAP, SECTION_GAP = 0.6, 1.8
PRONOUNCE = json.load(open(f"{REPO}/show/pronunciations.json"))


def clean(text):
    text = text.replace("’", "'").replace("“", '"').replace("”", '"')
    for pat, say in PRONOUNCE.items():
        text = re.sub(pat, say, text, flags=re.I)
    return text


def chunks(text):
    """Groups of whole paragraphs, about CHUNK_WORDS words; very long paragraphs split at sentences."""
    out, cur = [], []
    for para in [p.strip() for p in clean(text).split("\n") if p.strip()]:
        pieces = [para] if len(para.split()) <= CHUNK_WORDS * 1.5 else re.split(r"(?<=[.!?])\s+", para)
        for piece in pieces:
            if cur and len(" ".join(cur).split()) + len(piece.split()) > CHUNK_WORDS:
                out.append(" ".join(cur)); cur = []
            cur.append(piece)
        if cur and len(" ".join(cur).split()) >= CHUNK_WORDS * 0.6:
            out.append(" ".join(cur)); cur = []
    if cur:
        out.append(" ".join(cur))
    return out


def voice(text, dest, work):
    tmp = f"{work}/tmp"; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    base = [GEN, "--model", MODEL, "--text", text, "--output_path", tmp, "--file_prefix", "c", "--join_audio", "--ref_audio", REF]
    for cmd in (base + ["--ref_text", REF_TEXT], base):
        if subprocess.run(cmd, capture_output=True).returncode == 0:
            wavs = sorted(glob.glob(f"{tmp}/*.wav"))
            if wavs:
                subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wavs[-1], "-ar", "24000", "-ac", "1", dest], check=True)
                return True
    return False


def main():
    d = sys.argv[1]
    src = f"{REPO}/archive/{d[:4]}/{d[5:7]}/{d}/script"
    work = f"{HOME}/podcast/render_vox/{d}"; out = f"{HOME}/podcast/out"
    os.makedirs(work, exist_ok=True); os.makedirs(out, exist_ok=True)
    for name, secs in (("pgap", PARA_GAP), ("sgap", SECTION_GAP)):
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", str(secs), f"{work}/{name}.wav"], check=True)
    order, start, failed = [], time.time(), 0
    for f in sorted(glob.glob(f"{src}/*.txt")):
        sec = os.path.basename(f)[:-4]
        for i, text in enumerate(chunks(open(f).read())):
            dest = f"{work}/{sec}_{i:03d}.wav"
            if not os.path.exists(dest) and not voice(text, dest, work):
                print(f"FAILED: {sec} chunk {i}", flush=True); failed += 1; continue
            order += [dest, f"{work}/pgap.wav"]
        order[-1:] = [f"{work}/sgap.wav"]
        print(f"{sec} done, {int(time.time() - start)}s so far", flush=True)
    with open(f"{work}/list.txt", "w") as lst:
        lst.writelines(f"file '{p}'\n" for p in order)
    mp3 = f"{out}/Morning_Briefing_{d}.mp3"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{work}/list.txt",
                    *(["-af", SOFT] if CFG.get("soft_finish") else []), "-b:a", "128k", "-metadata", f"title=Morning Briefing - {d}", "-metadata", "artist=Morning Briefing", mp3], check=True)
    print(f"Done: {mp3} ({failed} chunks failed), {int(time.time() - start)}s")
    sys.exit(1 if failed > 3 else 0)


if __name__ == "__main__":
    main()
