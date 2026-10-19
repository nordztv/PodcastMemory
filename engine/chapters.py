"""Adds chapter markers and tags to a finished Morning Briefing MP3, so podcast apps can jump between segments.

Usage: python3 engine/chapters.py EPISODE.mp3 TIMINGS.txt DATE [headlines]
TIMINGS.txt has one line per section, in order: "<section file name><TAB><seconds incl. the gap after it>".
Starts are scaled to the MP3's real length, so slowing the audio down (VoxCPM2 pace) or encoder padding
never pushes the chapters out of line. The MP3 is rewritten in place (audio copied, not re-encoded).
"""
import os, subprocess, sys

TITLES = {
    "01_opening_world": "Good morning, weather and world news",
    "02_australia": "Australia, NSW and Sydney",
    "03_tech": "Tech",
    "04_games": "Games",
    "05_movies": "Movies",
    "06_lore": "Lore deep dive",
    "07_gametech": "Game tech deep dive",
    "08_effects": "Effects deep dive",
    "09_director": "Director deep dive",
    "10_workshop": "Workshop",
    "11_chat_outro": "Chat, workout and goodbye",
}


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", path],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def esc(s):
    return "".join("\\" + c if c in "=;#\\\n" else c for c in s)


def main():
    mp3, timings, date = sys.argv[1], sys.argv[2], sys.argv[3]
    headlines = len(sys.argv) > 4 and sys.argv[4] == "headlines"
    rows = []
    for line in open(timings):
        if line.strip():
            name, secs = line.rstrip("\n").split("\t")
            rows.append((name, float(secs)))
    total = duration(mp3)
    scale = total / sum(s for _, s in rows) if rows else 1.0
    title = f"Morning Briefing - {date}" + (" (headlines)" if headlines else "")
    meta = [";FFMETADATA1", f"title={esc(title)}", "artist=Morning Briefing", "album_artist=Morning Briefing",
            f"album={esc('Morning Briefing Headlines' if headlines else 'Morning Briefing')}", f"date={date}", "genre=Podcast"]
    t = 0.0
    if not headlines:
        for i, (name, secs) in enumerate(rows):
            start = int(t * 1000)
            t += secs * scale
            end = int(total * 1000) if i == len(rows) - 1 else int(t * 1000)
            label = TITLES.get(name, name.split("_", 1)[-1].replace("_", " ").capitalize())
            meta += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={start}", f"END={end}", f"title={esc(label)}"]
    meta_path = mp3 + ".meta.txt"; tmp = mp3 + ".tmp.mp3"
    open(meta_path, "w").write("\n".join(meta) + "\n")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", mp3, "-i", meta_path, "-map", "0:a", "-map_metadata", "1",
                    "-map_chapters", "1", "-c", "copy", "-id3v2_version", "3", tmp], check=True)
    os.replace(tmp, mp3); os.remove(meta_path)
    print(f"Chapters: {0 if headlines else len(rows)} added to {os.path.basename(mp3)}")


if __name__ == "__main__":
    main()
