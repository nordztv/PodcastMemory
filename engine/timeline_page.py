"""Builds Mizuki's life timeline page (Scott's feature 14, 12 Nov 2026) from her memory files.

Usage: python3 engine/timeline_page.py [OUT.html]   (default: ~/podcast/out/timeline.html)
Reads memory/mizuki_timeline.md, memory/mizuki_life.md (savings and energy), memory/mizuki_arcs.md,
memory/photo_log.md and memory/people_timelines.md. The daily run publishes it to the URL in show/timeline_url.txt
(Monday morning runs always; other runs when something changed). Like shownotes.py, the page has no doctype/head/body of its
own: the Artifact tool adds that skeleton when it publishes.
"""
import html, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(rel):
    try:
        with open(os.path.join(REPO, rel), encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def inline(s):
    s = html.escape(s.strip(), quote=True)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s


def money(s):
    m = re.search(r"\$([\d,]+)", s or "")
    return int(m.group(1).replace(",", "")) if m else None


def section(text, heading):
    m = re.search(rf"^## {re.escape(heading)}.*?$(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1) if m else ""


def table_rows(block):
    rows = []
    for line in block.splitlines():
        if line.startswith("|") and not re.match(r"^\|\s*-", line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            rows.append(cells)
    return rows[1:] if rows else []


# ---------- parse ----------
def parse_timeline():
    text = read("memory/mizuki_timeline.md")
    months, cur_month, cur_week = [], None, None
    for line in text.splitlines():
        if line.startswith("### "):
            cur_month = {"name": line[4:].strip(), "summary": [], "weeks": []}
            months.append(cur_month)
            cur_week = None
        elif line.startswith("#### ") and cur_month is not None:
            cur_week = {"name": line[5:].strip(), "days": [], "facts": []}
            cur_month["weeks"].append(cur_week)
        elif cur_month is not None and line.startswith("- "):
            m = re.match(r"- \*\*(.+?)\*\*\s*(.*)", line)
            if not m or cur_week is None:
                continue
            label, rest = m.group(1).rstrip(":"), m.group(2)
            if re.match(r"(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b", label):
                cur_week["days"].append((label, rest))
            else:
                cur_week["facts"].append((label, rest))
        elif cur_month is not None and cur_week is None and line.strip() and not line.startswith("#"):
            cur_month["summary"].append(line.strip())
    months.reverse()
    for mo in months:
        mo["weeks"].reverse()
    return months


def parse_life():
    text = read("memory/mizuki_life.md")
    funds = []
    for c in table_rows(section(text, "Savings")):
        if len(c) >= 4 and not c[0].startswith("**"):
            funds.append({"name": c[0], "saved": money(c[1]), "target": money(c[2]),
                          "keep": "keep" in c[2].lower(), "for": c[3]})
    total = re.search(r"^## Savings: (\$[\d,]+) \(as of ([^)]+)\)", text, re.M)
    energy_rows = [c for c in table_rows(section(text, "Energy")) if len(c) >= 3 and c[1].isdigit()]
    return funds, (total.group(1), total.group(2)) if total else ("", ""), energy_rows


def parse_arcs():
    text = section(read("memory/mizuki_arcs.md"), "Active")
    arcs = []
    for chunk in re.split(r"^### ", text, flags=re.M)[1:]:
        lines = chunk.splitlines()
        arc = {"name": lines[0].strip(), "intro": "", "stages": [], "now": "", "stage": 0, "log": []}
        mode = None
        for ln in lines[1:]:
            s = ln.strip()
            if s.startswith("- **Stages:**"):
                mode = "stages"
            elif s.startswith("- **Now:**"):
                arc["now"] = s[len("- **Now:**"):].strip()
                m = re.search(r"stage (\d+)", arc["now"])
                arc["stage"] = int(m.group(1)) if m else 0
                mode = None
            elif s.startswith("- **Log:**"):
                mode = "log"
            elif s.startswith("- **"):
                mode = None
            elif mode == "stages" and re.match(r"\d+\.", s):
                arc["stages"].append(re.sub(r"^\d+\.\s*", "", s))
            elif mode == "log" and s.startswith("- "):
                arc["log"].append(s[2:])
            elif s and not s.startswith("-") and not arc["intro"]:
                arc["intro"] = s
        arcs.append(arc)
    return arcs


def parse_photos():
    rows = table_rows(read("memory/photo_log.md"))
    return [r for r in rows if len(r) >= 5][::-1]


def parse_people_news():
    text = read("memory/people_timelines.md")
    news, who = [], None
    for ln in text.splitlines():
        m = re.match(r"- \*\*(.+?)(?: \(.*?\))?:\*\*", ln.strip())
        if m and not ln.startswith("  "):
            who = m.group(1)
        m2 = re.match(r"\s+- (\d{4}-\d{2}-\d{2}): (.*)", ln)
        if m2 and who:
            news.append((m2.group(1), who, m2.group(2)))
    return sorted(news, reverse=True)[:8]


# ---------- render ----------
CSS = """
/* Layout: one calm column, like her notebook; an indigo noren band on top, a red hanko stamp marking "now". */
:root{
  --paper:#f5f6fa; --sheet:#ffffff; --ink:#1d2340; --muted:#5d6482; --rule:#dfe2ee;
  --indigo:#2f3f86; --indigo-soft:#e6e9f6; --hanko:#c23b2f; --leaf:#3f7d5a;
  --display:"Zen Maru Gothic","Hiragino Maru Gothic ProN",system-ui,sans-serif;
  --body:"Noto Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
  --mono:"JetBrains Mono",ui-monospace,Menlo,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --paper:#11142a; --sheet:#181c36; --ink:#e8eaf6; --muted:#a3a9c9; --rule:#2a3054;
  --indigo:#9fb0ff; --indigo-soft:#232a52; --hanko:#ff7a6b; --leaf:#7cc79a; color-scheme:dark}}
:root[data-theme="dark"]{
  --paper:#11142a; --sheet:#181c36; --ink:#e8eaf6; --muted:#a3a9c9; --rule:#2a3054;
  --indigo:#9fb0ff; --indigo-soft:#232a52; --hanko:#ff7a6b; --leaf:#7cc79a; color-scheme:dark}
body{background:var(--paper);color:var(--ink);font-family:var(--body);font-size:15px;line-height:1.6}
.noren{background:var(--indigo);color:var(--sheet)}
:root:not([data-theme="light"]) .noren{color:var(--paper)}
.wrap{max-width:760px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.noren .wrap{padding-block:28px 22px}
.noren h1{font-family:var(--display);font-weight:700;font-size:clamp(28px,6vw,40px);margin:0;letter-spacing:.01em;text-wrap:balance}
.noren p{margin:4px 0 0;opacity:.85}
main.wrap{padding-block:24px 48px;display:grid;gap:36px}
h2{font-family:var(--display);font-size:20px;margin:0 0 12px;display:flex;align-items:baseline;gap:10px}
h2 small{font-family:var(--body);font-size:12px;color:var(--muted);font-weight:400;letter-spacing:.06em;text-transform:uppercase}
.now{display:grid;grid-template-columns:auto 1fr;gap:16px;align-items:center;background:var(--sheet);border:1px solid var(--rule);border-radius:10px;padding:16px}
.hanko{width:64px;height:64px;border:2.5px solid var(--hanko);color:var(--hanko);border-radius:50%;display:grid;place-items:center;font-family:var(--display);font-weight:700;font-size:13px;line-height:1.1;text-align:center;transform:rotate(-8deg)}
.meter{display:flex;gap:4px;margin:6px 0}
.meter i{width:18px;height:8px;border-radius:2px;background:var(--rule)}
.meter i.on{background:var(--leaf)}
.mood{font-style:italic;color:var(--muted);margin:0}
.funds{display:grid;gap:10px}
.fund{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:2px 12px}
.fund .bar{grid-column:1/-1;height:8px;background:var(--indigo-soft);border-radius:4px;overflow:hidden}
.fund .bar b{display:block;height:100%;background:var(--indigo)}
.fund .bar b.full{background:var(--leaf)}
.fund .num{font-family:var(--mono);font-size:13px;font-variant-numeric:tabular-nums;color:var(--muted)}
.fund .for{grid-column:1/-1;font-size:13px;color:var(--muted)}
.total{font-family:var(--mono);font-variant-numeric:tabular-nums}
.arcs{display:grid;gap:14px}
.arc{background:var(--sheet);border:1px solid var(--rule);border-radius:10px;padding:14px 16px;min-width:0}
.arc h3{font-family:var(--display);font-size:17px;margin:0 0 6px}
.steps{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0;padding:0;list-style:none}
.steps li{font-size:12px;padding:3px 9px;border-radius:999px;border:1px solid var(--rule);color:var(--muted)}
.steps li.done{background:var(--indigo-soft);color:var(--indigo);border-color:transparent}
.steps li.cur{background:var(--indigo);color:var(--sheet);border-color:var(--indigo);font-weight:600}
.arc p{margin:4px 0;font-size:14px}
.arc ul{margin:6px 0 0;padding-left:18px;font-size:13px;color:var(--muted)}
.photos{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}
.photo{background:var(--sheet);border:1px solid var(--rule);border-radius:4px;padding:12px 12px 14px;box-shadow:0 1px 0 var(--rule)}
.photo .frame{aspect-ratio:3/2;max-width:100%;border-radius:2px;background:linear-gradient(135deg,var(--indigo-soft),var(--rule));display:grid;place-items:center;font-family:var(--mono);font-size:11px;color:var(--muted);margin-bottom:10px;text-align:center;padding:8px}
.photo h3{font-family:var(--display);font-size:15px;margin:0 0 4px}
.photo p{margin:0;font-size:13px;color:var(--muted)}
.empty{color:var(--muted);font-size:14px;margin:0}
.news{list-style:none;margin:0;padding:0;display:grid;gap:8px}
.news li{display:grid;grid-template-columns:7.5em minmax(0,1fr);gap:10px;font-size:14px}
.news time{font-family:var(--mono);font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums;padding-top:2px}
.month{display:grid;gap:14px}
.month>h3{font-family:var(--display);font-size:18px;margin:8px 0 0;color:var(--indigo)}
.month .sum{margin:0;color:var(--muted)}
.week{border-left:2px solid var(--rule);padding-left:16px;display:grid;gap:8px;min-width:0}
.week h4{font-family:var(--display);font-size:15px;margin:0;position:relative}
.week h4::before{content:"";position:absolute;left:-22px;top:.45em;width:10px;height:10px;border-radius:50%;background:var(--paper);border:2px solid var(--indigo)}
.day{display:grid;grid-template-columns:7.5em minmax(0,1fr);gap:10px}
.day b{font-family:var(--mono);font-size:12px;font-weight:500;color:var(--indigo);padding-top:3px}
.facts{display:grid;gap:4px;font-size:14px;color:var(--muted);background:var(--sheet);border:1px solid var(--rule);border-radius:8px;padding:10px 12px}
.facts strong{color:var(--ink)}
code{font-family:var(--mono);font-size:.9em}
@media (max-width:480px){.day,.news li{grid-template-columns:1fr;gap:0}}
"""


def render():
    months = parse_timeline()
    funds, (total, as_of), energy = parse_life()
    arcs = parse_arcs()
    photos = parse_photos()
    news = parse_people_news()
    out = ['<title>Mizuki\'s Life</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n',
           '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
           '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500;700&family=Noto+Sans:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap">',
           f"<style>{CSS}</style>",
           '<header class="noren"><div class="wrap"><h1>Mizuki\'s Life</h1>',
           '<p>Mizuki Tanaka, 36, Pyrmont. Her life week by week since 9 November 2026: the good, the bad and the savings.</p></div></header>',
           '<main class="wrap">']

    # Now
    mood = ""
    for mo in months:
        for wk in mo["weeks"]:
            for label, text in wk["facts"]:
                if label.lower().startswith("mood") and not mood:
                    mood = text
    level, why, when = (int(energy[-1][1]), energy[-1][2], energy[-1][0]) if energy else (0, "", "")
    meter = "".join(f'<i class="{"on" if i < level else ""}"></i>' for i in range(10))
    out.append('<section><h2>Right now <small>' + html.escape(when) + '</small></h2><div class="now">'
               '<div class="hanko">今<br>now</div><div style="min-width:0">'
               f'<div><strong>Energy {level}/10</strong></div><div class="meter" role="img" aria-label="Energy {level} out of 10">{meter}</div>'
               f'<p style="margin:0 0 4px;font-size:14px">{inline(why)}</p>'
               + (f'<p class="mood">{inline(mood)}</p>' if mood else "") + '</div></div></section>')

    # Savings
    rows = []
    for f in funds:
        saved, target = f["saved"] or 0, f["target"] or 0
        pct = min(100, round(100 * saved / target)) if target else 0
        full = "full" if pct >= 100 else ""
        right = f"${saved:,}" + ("" if f["keep"] else f" of ${target:,}")
        rows.append(f'<div class="fund"><strong>{inline(f["name"])}</strong><span class="num">{right}</span>'
                    f'<div class="bar"><b class="{full}" style="width:{pct}%"></b></div><span class="for">{inline(f["for"])}</span></div>')
    out.append(f'<section><h2>Savings <small>as of {html.escape(as_of)}</small></h2>'
               f'<p class="total" style="margin:0 0 12px">Total {html.escape(total)}</p><div class="funds">{"".join(rows)}</div></section>')

    # Arcs
    cards = []
    for a in arcs:
        steps = "".join(
            f'<li class="{"cur" if i + 1 == a["stage"] else ("done" if i + 1 < a["stage"] else "")}">{inline(s)}</li>'
            for i, s in enumerate(a["stages"]))
        log = "".join(f"<li>{inline(l)}</li>" for l in a["log"][-3:][::-1])
        cards.append(f'<article class="arc"><h3>{inline(a["name"])}</h3>'
                     + (f"<p>{inline(a['intro'])}</p>" if a["intro"] else "")
                     + (f'<ol class="steps">{steps}</ol>' if steps else "")
                     + (f"<p><strong>Now:</strong> {inline(a['now'])}</p>" if a["now"] else "")
                     + (f"<ul>{log}</ul>" if log else "") + "</article>")
    out.append('<section><h2>Her long stories <small>moves only when life does</small></h2><div class="arcs">'
               + "".join(cards) + "</div></section>")

    # Photos
    if photos:
        cards = []
        for r in photos[:6]:
            date, title, what, cam = r[0], r[1], r[2], r[3]
            pick = len(r) > 5 and r[5].strip() not in ("", "no", "-")
            cards.append(f'<article class="photo"><div class="frame">{inline(cam)}</div>'
                         f'<h3>{inline(title)}{" · Photo of the Month" if pick else ""}</h3><p>{inline(date)} · {inline(what)}</p></article>')
        out.append('<section><h2>Photos <small>her photo of the week</small></h2><div class="photos">' + "".join(cards) + "</div></section>")
    else:
        out.append('<section><h2>Photos <small>her photo of the week</small></h2><p class="empty">Her first photo of the week arrives on Friday.</p></section>')

    # People news
    if news:
        items = "".join(f"<li><time>{d}</time><span><strong>{inline(w)}</strong>: {inline(t)}</span></li>" for d, w, t in news)
        out.append(f'<section><h2>News from her people</h2><ul class="news">{items}</ul></section>')

    # Timeline
    tl = ['<section><h2>Timeline <small>newest first</small></h2>']
    for mo in months:
        tl.append(f'<div class="month"><h3>{inline(mo["name"])}</h3>')
        if mo["summary"]:
            tl.append(f'<p class="sum">{inline(" ".join(mo["summary"]))}</p>')
        for wk in mo["weeks"]:
            days = "".join(f'<div class="day"><b>{inline(l)}</b><span>{inline(t[:1].upper() + t[1:])}</span></div>' for l, t in reversed(wk["days"]))
            facts = "".join(f"<div><strong>{inline(l)}:</strong> {inline(t)}</div>" for l, t in wk["facts"])
            tl.append(f'<div class="week"><h4>{inline(wk["name"])}</h4>{days}'
                      + (f'<div class="facts">{facts}</div>' if facts else "") + "</div>")
        tl.append("</div>")
    tl.append("</section>")
    out.extend(tl)
    out.append("</main>")
    return "\n".join(out)


def main():
    dest = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/podcast/out/timeline.html")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(render())
    print(dest)


if __name__ == "__main__":
    main()
