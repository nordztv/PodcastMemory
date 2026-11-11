"""Mood music for Morning Briefing: quiet, original background cues under the emotional moments only.

Usage: python3 engine/music.py VOICE.mp3 OUT.mp3
Reads VOICE.moods.json (written by engine/tts.py next to its MP3: each spoken chunk's start, end, mood and punch flag)
and mixes in music that the script itself synthesises (no samples, nothing to download, no licensing):
  - dark (sweet spooky, horror picks, dark bits): a slow minor music box over a low, breathing drone
  - whisper (whispered secrets): a soft, high shimmer with a little air
  - punch lines in a cheeky stretch (jokes and teases): a tiny two-note pizzicato "ba-dum" in the pause after
Everything else (news, normal talk) gets no music. Each cue lasts only as long as its moment, plus a short tail,
fades in and out, and has the speech band (about 1 to 3.5 kHz) carved out so her voice stays clear.
"""
import json, os, subprocess, sys
import numpy as np
from scipy.signal import butter, sosfilt

SR = 24000
rng = np.random.default_rng(7)


def note(n):  # MIDI note -> Hz
    return 440.0 * 2 ** ((n - 69) / 12)


def env(n, attack, decay):
    t = np.arange(n) / SR
    return np.minimum(t / max(attack, 1e-4), 1) * np.exp(-t / decay)


def reverb(x, size=1.6, mix=0.35):
    n = int(SR * size)
    ir = rng.standard_normal(n) * np.exp(-np.arange(n) / (SR * size / 5))
    ir = sosfilt(butter(2, 4000, "low", fs=SR, output="sos"), ir)
    wet = np.convolve(x, ir)[: len(x)]
    wet *= np.max(np.abs(x)) / (np.max(np.abs(wet)) + 1e-9)
    return (1 - mix) * x + mix * wet


def music_box(length):
    """Slow A minor music-box figure: bell-like partials, each note ringing out."""
    out = np.zeros(length)
    melody = [81, 84, 88, 86, 84, 83, 81, 76, 77, 81, 80, 76]   # A5 C6 E6 D6 C6 B5 A5 E5 F5 A5 G#5 E5
    step, i, t0 = 0.62, 0, int(SR * 0.15)
    while t0 < length:
        f = note(melody[i % len(melody)]) * (1 + rng.uniform(-0.002, 0.002))   # a slightly worn music box
        n = min(int(SR * 2.2), length - t0)
        t = np.arange(n) / SR
        tone = sum(a * np.sin(2 * np.pi * f * r * t) for r, a in [(1, 1), (2.76, 0.32), (5.4, 0.12), (8.9, 0.05)])
        out[t0:t0 + n] += tone * env(n, 0.003, 0.55) * (0.9 if i % 4 else 1.0)
        t0 += int(SR * step * (1.5 if i % 6 == 5 else 1)); i += 1
    return reverb(out, 1.8, 0.4)


def drone(length):
    t = np.arange(length) / SR
    lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.18 * t)            # slow breathing
    d = np.sin(2 * np.pi * note(45) * t) + 0.5 * np.sin(2 * np.pi * note(52) * t) + 0.25 * np.sin(2 * np.pi * note(57) * 1.003 * t)
    return d * lfo


def shimmer(length):
    t = np.arange(length) / SR
    out = np.zeros(length)
    for k, n in enumerate([88, 95, 100, 107]):                 # E6 B6 E7 B7, each swelling at its own pace
        out += np.sin(2 * np.pi * note(n) * t) * (0.5 + 0.5 * np.sin(2 * np.pi * (0.11 + 0.07 * k) * t + k)) / (k + 1.5)
    air = sosfilt(butter(2, [6000, 10000], "band", fs=SR, output="sos"), rng.standard_normal(length)) * 0.15
    return reverb(out + air, 2.2, 0.5)


def pluck(f, dur=0.5):
    """Karplus-Strong plucked string."""
    n, p = int(SR * dur), int(SR / f)
    buf, out = rng.uniform(-1, 1, p), np.zeros(int(SR * dur))
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = 0.996 * 0.5 * (buf[i % p] + buf[(i + 1) % p])
    return out


def sting():
    a, b = pluck(note(55), 0.45), pluck(note(62), 0.7)       # G3 ... D4: "ba-dum"
    out = np.zeros(int(SR * 1.0))
    out[: len(a)] += a
    out[int(SR * 0.22): int(SR * 0.22) + len(b)] += b * 1.2
    return reverb(out, 0.8, 0.25)


def fade(x, fin, fout):
    n = len(x)
    e = np.ones(n)
    a, b = min(int(SR * fin), n // 2), min(int(SR * fout), n // 2)
    e[:a] = np.linspace(0, 1, a) ** 2
    e[n - b:] = np.linspace(1, 0, b) ** 2
    return x * e


def carve(x):
    """Pull the music out of the speech band so the voice sits on top."""
    band = sosfilt(butter(2, [900, 3500], "band", fs=SR, output="sos"), x)
    return x - 0.8 * band


def regions(spans, mood, lead=0.4, tail=1.2, join=1.5):
    """Merge consecutive spans of one mood into moments (gaps under `join` seconds are bridged)."""
    out = []
    for s in spans:
        if s["mood"] != mood:
            continue
        if out and s["start"] - out[-1][1] < join:
            out[-1][1] = s["end"]
        else:
            out.append([s["start"], s["end"]])
    return [(max(0, a - lead), b + tail) for a, b in out]


def level(x, peak):
    return x * peak / (np.max(np.abs(x)) + 1e-9)


def load(path):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def main():
    src, out = sys.argv[1], sys.argv[2]
    spans = json.load(open(os.path.splitext(src)[0] + ".moods.json"))
    voice = load(src)
    bed = np.zeros(len(voice) + SR * 3)
    for a, b in regions(spans, "dark"):
        i, n = int(a * SR), int((b - a) * SR)
        cue = level(music_box(n), 0.07) + level(drone(n), 0.045)
        bed[i:i + n] += fade(carve(cue), 1.0, 1.4)
    for a, b in regions(spans, "whisper", tail=1.5):
        i, n = int(a * SR), int((b - a) * SR)
        bed[i:i + n] += fade(carve(level(shimmer(n), 0.16)), 1.2, 1.6)
    cheeky = [s for s in spans if s["punch"] and s["mood"] == "cheeky"]
    for s in cheeky:
        i, st = int((s["end"] + 0.05) * SR), level(sting(), 0.09)
        bed[i:i + len(st)] += st[: len(bed) - i]
    mix = np.concatenate([voice, np.zeros(len(bed) - len(voice))]) + bed
    mix = mix[: len(voice) + int(SR * 0.5)]
    pcm = (np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-",
                    "-b:a", "128k", out], input=pcm, check=True)
    print(f"{out}: {len(mix) / SR:.1f}s, {len(regions(spans, 'dark'))} spooky, "
          f"{len(regions(spans, 'whisper'))} secret, {len(cheeky)} joke cues")


if __name__ == "__main__":
    main()
