"""Builds the Morning Briefing show-notes page (one HTML page, newest episode first) from each episode's shownotes.json.

Usage: python3 engine/shownotes.py [OUT.html]   (default: ~/podcast/out/shownotes.html)
Reads archive/*/*/*/shownotes.json (the newest 15 episodes). The daily run writes shownotes.json and publishes the
page to Scott's show-notes artifact (URL in show/shownotes_url.txt). The page has no doctype/head/body of its own:
the Artifact tool adds that skeleton when it publishes.

shownotes.json:
{
  "date": "2026-10-21", "weekday": "Wednesday", "length": "78 min", "headline": "one line on the day",
  "segments": [ {"name": "Tech", "items": [ {"title": "Short story title", "note": "one line, optional",
                                            "links": [ {"label": "Reuters", "url": "https://..."} ] } ] } ],
  "picks": [ {"kind": "Retro Game of the Week", "title": "...", "note": "...", "links": [...]} ],
  "questions": ["..."]
}
"""
import glob, html, json, os, sys
from urllib.parse import urlparse

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEEP = 15


def esc(s):
    return html.escape(str(s or ""), quote=True)


def host(url):
    h = urlparse(url).netloc.lower()
    return h[4:] if h.startswith("www.") else h


def links(ls):
    if not ls:
        return ""
    out = []
    for l in ls:
        url = l.get("url", "")
        if not url.startswith(("https://", "http://")):
            continue
        label = l.get("label") or host(url)
        out.append(f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}<span class="src">{esc(host(url))}</span></a>')
    return f'<div class="links">{"".join(out)}</div>' if out else ""


def item(it):
    note = f'<p class="note">{esc(it["note"])}</p>' if it.get("note") else ""
    return f'<li><h4>{esc(it.get("title"))}</h4>{note}{links(it.get("links"))}</li>'


def episode(ep, latest):
    d = ep["date"]
    eid = "e" + d.replace("-", "")
    meta = esc(ep.get("length", ""))
    segs = []
    for i, s in enumerate(ep.get("segments", []), 1):
        items = "".join(item(it) for it in s.get("items", []))
        summary = f'<p class="note">{esc(s["summary"])}</p>' if s.get("summary") else ""
        segs.append(f'<section class="seg"><h3><span class="n">{i:02d}</span>{esc(s.get("name"))}</h3>{summary}'
                    f'{f"<ul>{items}</ul>" if items else ""}{links(s.get("links"))}</section>')
    def pick(p):
        note = f'<p class="note">{esc(p["note"])}</p>' if p.get("note") else ""
        return (f'<div class="pick"><span class="kind">{esc(p.get("kind"))}</span><h4>{esc(p.get("title"))}</h4>'
                f'{note}{links(p.get("links"))}</div>')
    picks = "".join(pick(p) for p in ep.get("picks", []))
    qs = "".join(f"<li>{esc(q)}</li>" for q in ep.get("questions", []))
    body = (f'{f"<div class=picks>{picks}</div>" if picks else ""}'
            f'<div class="segs">{"".join(segs)}</div>'
            f'{f"<section class=qs><h3>Today&#39;s questions for you</h3><ol>{qs}</ol></section>" if qs else ""}')
    head = (f'<span class="date">{esc(ep.get("weekday", ""))} {esc(d)}</span>'
            f'<span class="headline">{esc(ep.get("headline", ""))}</span><span class="meta">{meta}</span>')
    return f'<details class="ep" id="{eid}"{" open" if latest else ""}><summary>{head}</summary><div class="body">{body}</div></details>'


CSS = """
/* Layout: one reading column, newest episode first and open, older episodes as collapsed disclosures */
:root{
  --bg:#eef2f4; --surface:#ffffff; --ink:#17232b; --muted:#5a6a74; --line:#d4dde2; --accent:#c96a1e; --accent-soft:#fbe9da;
  --display:"Bricolage Grotesque", "Avenir Next", system-ui, sans-serif;
  --body:"Atkinson Hyperlegible", system-ui, -apple-system, sans-serif;
  --mono:"JetBrains Mono", ui-monospace, Menlo, monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#0f161b; --surface:#16212a; --ink:#e5ecf0; --muted:#97a8b2; --line:#26353f; --accent:#f0a35e; --accent-soft:#2c2116; color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0f161b; --surface:#16212a; --ink:#e5ecf0; --muted:#97a8b2; --line:#26353f; --accent:#f0a35e; --accent-soft:#2c2116; color-scheme:dark}
body{background:var(--bg); color:var(--ink); font:16px/1.55 var(--body)}
.wrap{max-width:760px; margin:0 auto; padding-block:28px 56px; padding-left:max(16px, env(safe-area-inset-left, 0px)); padding-right:max(16px, env(safe-area-inset-right, 0px)); display:grid; gap:18px}
header h1{font:700 clamp(28px,6vw,40px)/1.05 var(--display); letter-spacing:-.01em; margin:0; text-wrap:balance}
header p{margin:6px 0 0; color:var(--muted)}
.ep{background:var(--surface); border:1px solid var(--line); border-radius:12px}
.ep summary{cursor:pointer; list-style:none; padding:16px 18px; display:grid; gap:2px}
.ep summary::-webkit-details-marker{display:none}
.ep summary:focus-visible{outline:2px solid var(--accent); outline-offset:2px; border-radius:12px}
.date{font:500 12px/1.4 var(--mono); text-transform:uppercase; letter-spacing:.06em; color:var(--accent)}
.headline{font:600 19px/1.3 var(--display); text-wrap:balance}
.meta{font:13px/1.4 var(--mono); color:var(--muted); font-variant-numeric:tabular-nums}
.ep[open] summary{border-bottom:1px solid var(--line)}
.body{padding:6px 18px 18px; display:grid; gap:18px}
.picks{display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr)); gap:10px; padding-top:12px}
.pick{background:var(--accent-soft); border-radius:10px; padding:12px 14px; min-width:0}
.kind{font:500 11px/1.4 var(--mono); text-transform:uppercase; letter-spacing:.07em; color:var(--accent)}
.pick h4{margin:2px 0 0; font:600 17px/1.3 var(--display)}
.segs{display:grid; gap:4px}
.seg{padding-top:12px; border-top:1px solid var(--line); min-width:0}
.seg:first-child{border-top:0}
.seg h3,.qs h3{margin:0 0 6px; font:600 15px/1.3 var(--display); display:flex; gap:10px; align-items:baseline}
.n{font:500 12px var(--mono); color:var(--muted)}
.seg ul{list-style:none; margin:0; padding:0; display:grid; gap:10px}
.seg h4{margin:0; font:600 15.5px/1.4 var(--body)}
.note{margin:2px 0 0; color:var(--muted); font-size:15px; max-width:65ch}
.links{display:flex; flex-wrap:wrap; gap:6px 12px; margin-top:4px}
.links a{color:var(--ink); text-decoration:underline; text-decoration-color:var(--accent); text-underline-offset:3px; font-size:14.5px; overflow-wrap:anywhere}
.links a:hover{color:var(--accent)}
.links a:focus-visible{outline:2px solid var(--accent); outline-offset:2px}
.src{color:var(--muted); font:12px var(--mono); margin-left:6px; text-decoration:none; display:inline-block}
.qs ol{margin:0; padding-left:22px; display:grid; gap:6px}
footer{color:var(--muted); font-size:13px}
"""


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/podcast/out/shownotes.html")
    eps = []
    for f in sorted(glob.glob(f"{REPO}/archive/*/*/*/shownotes.json"), reverse=True)[:KEEP]:
        try:
            eps.append(json.load(open(f)))
        except Exception as e:
            print(f"skipped {f}: {e}")
    eps.sort(key=lambda e: e.get("date", ""), reverse=True)
    page = ('<title>Morning Briefing Show Notes</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,700&family=JetBrains+Mono:wght@400;500&display=swap">\n'
            f'<style>{CSS}</style>\n<div class="wrap"><header><h1>Morning Briefing</h1>'
            '<p>Links and picks from each episode, newest first. Tap an episode to open it.</p></header>\n'
            + "\n".join(episode(e, i == 0) for i, e in enumerate(eps))
            + '\n<footer>Updated each weekday morning with the new episode.</footer></div>\n')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(page)
    print(f"Show notes: {len(eps)} episodes -> {out}")


if __name__ == "__main__":
    main()
