#!/usr/bin/env python3
"""Render the MST400 study guide markdown into the study page HTML."""

import html
import re
from pathlib import Path

import markdown

HERE = Path(__file__).parent
SRC = HERE / "MST400-Final-Exam-Study-Guide.md"
OUT = HERE / "mst400-study-guide.html"

STYLE = """
:root {
  color-scheme: light dark;

  --ground:  #f3f6f6;
  --surface: #ffffff;
  --sunken:  #eaeff0;
  --ink:     #131a1c;
  --muted:   #56676a;
  --faint:   #7d8f92;
  --rule:    #d7e0e0;
  --rule-soft: #e6eded;
  --accent:  #0e6e75;
  --accent-soft: #dbedee;
  --flag:    #a2400f;
  --flag-soft: #f7e6dc;

  --font-display: Georgia, "Iowan Old Style", "Source Serif 4", "Times New Roman", serif;
  --font-body: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
  --font-mono: ui-monospace, "SF Mono", "Cascadia Mono", Menlo, Consolas, monospace;

  --measure: 68ch;
  --rail: 16.5rem;
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --ground:  #0e1416;
    --surface: #151d20;
    --sunken:  #1b2427;
    --ink:     #e3eaea;
    --muted:   #93a4a6;
    --faint:   #74868a;
    --rule:    #253133;
    --rule-soft: #1e282b;
    --accent:  #4ec3ca;
    --accent-soft: #10393c;
    --flag:    #f0975f;
    --flag-soft: #3a2318;
  }
}

:root[data-theme="dark"] {
  --ground:  #0e1416;
  --surface: #151d20;
  --sunken:  #1b2427;
  --ink:     #e3eaea;
  --muted:   #93a4a6;
  --faint:   #74868a;
  --rule:    #253133;
  --rule-soft: #1e282b;
  --accent:  #4ec3ca;
  --accent-soft: #10393c;
  --flag:    #f0975f;
  --flag-soft: #3a2318;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--ground);
  color: var(--ink);
  font-family: var(--font-body);
  font-size: 16px;
  line-height: 1.65;
  -webkit-text-size-adjust: 100%;
}

/* ---------- shell ---------- */

.shell {
  display: grid;
  grid-template-columns: var(--rail) minmax(0, 1fr);
  align-items: start;
  gap: 0;
  max-width: 78rem;
  margin: 0 auto;
}

.rail {
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  padding: 2.5rem 1.5rem 3rem 1.75rem;
  border-right: 1px solid var(--rule);
  background: var(--ground);
}

.rail__brand {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--accent);
  margin: 0 0 0.35rem;
}

.rail__title {
  font-family: var(--font-display);
  font-size: 1.05rem;
  line-height: 1.3;
  margin: 0 0 1.5rem;
  font-weight: 600;
}

.rail nav ol {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  counter-reset: navitem;
}

.rail nav a {
  display: grid;
  grid-template-columns: 1.9rem 1fr;
  gap: 0.35rem;
  align-items: baseline;
  padding: 0.3rem 0.45rem 0.3rem 0;
  font-size: 0.82rem;
  line-height: 1.35;
  color: var(--muted);
  text-decoration: none;
  border-radius: 3px;
}

.rail nav a::before {
  counter-increment: navitem;
  content: counter(navitem, decimal-leading-zero);
  font-family: var(--font-mono);
  font-size: 0.68rem;
  color: var(--faint);
  letter-spacing: 0.03em;
}

.rail nav a:hover,
.rail nav a:focus-visible { color: var(--ink); }
.rail nav a:hover::before { color: var(--accent); }

.rail nav a.is-current {
  color: var(--accent);
  font-weight: 600;
}
.rail nav a.is-current::before { color: var(--accent); }

.main {
  padding: 0 3.5rem 8rem;
  min-width: 0;
}

.wrap { max-width: var(--measure); }

/* ---------- masthead ---------- */

.masthead {
  padding: 4.5rem 0 2.25rem;
  border-bottom: 2px solid var(--ink);
  margin-bottom: 2.5rem;
}

.masthead__eyebrow {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--accent);
  margin: 0 0 1rem;
}

.masthead h1 {
  font-family: var(--font-display);
  font-size: clamp(2.1rem, 4.2vw, 3.1rem);
  line-height: 1.08;
  letter-spacing: -0.015em;
  font-weight: 600;
  margin: 0 0 1rem;
  text-wrap: balance;
}

.masthead p {
  color: var(--muted);
  max-width: 52ch;
  margin: 0 0 1.75rem;
  font-size: 1.02rem;
}

.facts {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(9rem, 1fr));
  gap: 1px;
  background: var(--rule);
  border: 1px solid var(--rule);
}

.facts div {
  background: var(--surface);
  padding: 0.85rem 1rem;
}

.facts dt {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--faint);
  margin: 0 0 0.3rem;
}

.facts dd {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}

/* ---------- prose ---------- */

.prose { max-width: var(--measure); }

.prose h2 {
  font-family: var(--font-display);
  font-size: 1.85rem;
  line-height: 1.18;
  letter-spacing: -0.01em;
  font-weight: 600;
  margin: 4.5rem 0 1.25rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--rule);
  scroll-margin-top: 1.5rem;
  text-wrap: balance;
}

.prose h2:first-child { margin-top: 0; border-top: 0; padding-top: 0; }

.prose h3 {
  font-family: var(--font-display);
  font-size: 1.22rem;
  font-weight: 600;
  line-height: 1.3;
  margin: 2.75rem 0 0.85rem;
  scroll-margin-top: 1.5rem;
  text-wrap: balance;
}

.prose h4 {
  font-family: var(--font-mono);
  font-size: 0.74rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--accent);
  margin: 2rem 0 0.6rem;
  font-weight: 600;
}

.prose p { margin: 0 0 1.1rem; }

.prose a {
  color: var(--accent);
  text-decoration: none;
  border-bottom: 1px solid color-mix(in srgb, var(--accent) 35%, transparent);
}
.prose a:hover { border-bottom-color: var(--accent); }

.prose ul, .prose ol {
  margin: 0 0 1.2rem;
  padding-left: 1.35rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.prose li { padding-left: 0.15rem; }
.prose li > ul, .prose li > ol { margin: 0.4rem 0 0; }

.prose strong { font-weight: 650; }

.prose hr {
  border: 0;
  border-top: 1px solid var(--rule);
  margin: 3rem 0;
}

/* inline code + blocks: the guide's data voice */

.prose code {
  font-family: var(--font-mono);
  font-size: 0.855em;
  background: var(--sunken);
  border: 1px solid var(--rule-soft);
  border-radius: 3px;
  padding: 0.08em 0.34em;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}

.prose pre {
  background: var(--sunken);
  border: 1px solid var(--rule);
  border-left: 3px solid var(--accent);
  padding: 1rem 1.15rem;
  overflow-x: auto;
  margin: 0 0 1.4rem;
  line-height: 1.55;
}

.prose pre code {
  background: none;
  border: 0;
  padding: 0;
  font-size: 0.83rem;
  white-space: pre;
}

/* callouts — blockquotes carry the exam-trick warnings */

.prose blockquote {
  margin: 1.4rem 0;
  padding: 0.9rem 1.1rem;
  background: var(--flag-soft);
  border-left: 3px solid var(--flag);
  color: var(--ink);
  font-size: 0.95rem;
}

.prose blockquote p:last-child { margin-bottom: 0; }
.prose blockquote strong { color: var(--flag); }
.prose blockquote code { background: color-mix(in srgb, var(--flag) 12%, transparent); border-color: transparent; }

/* tables — the reference spine */

.table-scroll {
  overflow-x: auto;
  margin: 0 0 1.6rem;
  border: 1px solid var(--rule);
  background: var(--surface);
}

.prose table {
  border-collapse: collapse;
  width: 100%;
  font-size: 0.895rem;
  line-height: 1.5;
}

.prose thead th {
  text-align: left;
  vertical-align: bottom;
  font-family: var(--font-mono);
  font-size: 0.66rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--faint);
  font-weight: 600;
  padding: 0.7rem 0.9rem;
  border-bottom: 1px solid var(--rule);
  background: var(--sunken);
  white-space: nowrap;
}

.prose tbody td,
.prose tbody th {
  padding: 0.65rem 0.9rem;
  border-bottom: 1px solid var(--rule-soft);
  vertical-align: top;
  text-align: left;
  font-weight: inherit;
}

.prose tbody tr:last-child td { border-bottom: 0; }

.prose tbody td:first-child {
  font-variant-numeric: tabular-nums;
}

.prose tbody td code { white-space: nowrap; }

/* practice reveals */

details.reveal {
  border: 1px solid var(--rule);
  border-left: 3px solid var(--accent);
  background: var(--surface);
  margin: 0 0 1.1rem;
}

details.reveal > summary {
  cursor: pointer;
  padding: 0.6rem 0.95rem;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  letter-spacing: 0.11em;
  text-transform: uppercase;
  color: var(--accent);
  list-style: none;
  user-select: none;
}

details.reveal > summary::-webkit-details-marker { display: none; }
details.reveal > summary::before { content: "▸ "; }
details.reveal[open] > summary::before { content: "▾ "; }
details.reveal > summary:hover { background: var(--sunken); }

details.reveal .reveal__body {
  padding: 0.25rem 1.1rem 0.4rem;
  border-top: 1px solid var(--rule-soft);
  font-size: 0.95rem;
}

details.reveal .reveal__body p:first-child { margin-top: 0.9rem; }

.qnum {
  font-family: var(--font-mono);
  color: var(--accent);
}

.mcq { margin: 0 0 0.3rem; }

.mco {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(13rem, 1fr));
  gap: 0.3rem 1.6rem;
  margin: 0 0 1.5rem;
  padding-left: 1.9rem;
  color: var(--muted);
  font-size: 0.94rem;
}

.mco span { display: block; }
.mco b {
  font-family: var(--font-mono);
  font-size: 0.82em;
  font-weight: 600;
  color: var(--faint);
  margin-right: 0.3em;
}

.answer-key {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  line-height: 2;
  word-spacing: 0.15em;
}

/* ---------- theme toggle ---------- */

.themer {
  position: fixed;
  right: 1.25rem;
  bottom: 1.25rem;
  z-index: 20;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 0.8rem;
  background: var(--surface);
  border: 1px solid var(--rule);
  border-radius: 999px;
  color: var(--muted);
  font-family: var(--font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  cursor: pointer;
}

.themer:hover { color: var(--ink); border-color: var(--accent); }

:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

.skip {
  position: absolute;
  left: -9999px;
}
.skip:focus {
  left: 1rem;
  top: 1rem;
  z-index: 40;
  background: var(--surface);
  border: 1px solid var(--accent);
  padding: 0.5rem 0.9rem;
  color: var(--ink);
}

/* ---------- responsive ---------- */

@media (max-width: 60rem) {
  .shell { grid-template-columns: 1fr; }
  .rail {
    position: static;
    height: auto;
    border-right: 0;
    border-bottom: 1px solid var(--rule);
    padding: 1.75rem 1.5rem;
  }
  .rail nav ol {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(13rem, 1fr));
    gap: 0.1rem 1rem;
  }
  .main { padding: 0 1.5rem 5rem; }
  .masthead { padding-top: 2.5rem; }
}

@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; scroll-behavior: auto !important; }
}

@media print {
  .rail, .themer { display: none; }
  .shell { grid-template-columns: 1fr; }
  body { background: #fff; color: #000; }
}
"""

SCRIPT = """
(function () {
  var root = document.documentElement;
  var btn = document.querySelector('.themer');
  var label = btn.querySelector('span');

  function apply(mode) {
    if (mode === 'system') { root.removeAttribute('data-theme'); }
    else { root.setAttribute('data-theme', mode); }
    label.textContent = mode;
  }

  var order = ['system', 'light', 'dark'];
  var current = 'system';
  btn.addEventListener('click', function () {
    current = order[(order.indexOf(current) + 1) % order.length];
    apply(current);
  });

  var links = Array.prototype.slice.call(document.querySelectorAll('.rail nav a'));
  var targets = links
    .map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); })
    .filter(Boolean);

  if ('IntersectionObserver' in window) {
    var seen = new Map();
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { seen.set(e.target.id, e.intersectionRatio > 0); });
      var activeId = null;
      for (var i = 0; i < targets.length; i++) {
        if (seen.get(targets[i].id)) { activeId = targets[i].id; break; }
      }
      if (!activeId) return;
      links.forEach(function (a) {
        a.classList.toggle('is-current', a.getAttribute('href') === '#' + activeId);
      });
    }, { rootMargin: '0px 0px -75% 0px' });
    targets.forEach(function (t) { io.observe(t); });
  }
})();
"""


def slugify(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text).lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    return re.sub(r"\s+", "-", text.strip())


def loosen_lists(text: str) -> str:
    """Insert the blank line python-markdown needs before a list that follows a paragraph.

    The source reads fine on GitHub, which lets a list interrupt a paragraph; without
    this the bullets get swallowed into the preceding <p>.
    """
    lines = text.split("\n")
    out: list[str] = []
    in_fence = False
    for line in lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        is_item = bool(re.match(r"\s*([-*+]|\d+\.)\s+", line))
        if (
            not in_fence
            and is_item
            and out
            and out[-1].strip()
            and not re.match(r"\s*([-*+]|\d+\.)\s+", out[-1])
            and not out[-1].lstrip().startswith((">", "|", "#"))
        ):
            out.append("")
        out.append(line)
    return "\n".join(out)


def md(text: str) -> str:
    """Render a markdown fragment to HTML."""
    return markdown.markdown(
        loosen_lists(text.strip()), extensions=["tables", "fenced_code", "sane_lists"]
    )


def md_inline(text: str) -> str:
    """Render a short inline-only markdown fragment."""
    return re.sub(r"^<p>|</p>$", "", md(text).strip())


def build_multiple_choice(md_text: str) -> str:
    """Split each '**n.** question / A) B) C) D)' pair onto its own line."""
    out = []
    for chunk in re.split(r"\n\n+", md_text.strip()):
        m = re.match(r"\*\*(\d+)\.\*\*\s*(.+?)\n([A-D]\).+)$", chunk.strip(), re.S)
        if not m:
            out.append(md(chunk))
            continue
        num, question, options = m.groups()
        parts = re.split(r"\s(?=[A-D]\)\s)", options.replace("\n", " ").strip())
        opts = "".join(
            f"<span><b>{p[0]}</b>{md_inline(p[2:].strip())}</span>" for p in parts
        )
        out.append(
            f'<p class="mcq"><strong><span class="qnum">{num}.</span></strong> '
            f'{md_inline(question)}</p><p class="mco">{opts}</p>'
        )
    return "\n".join(out)


def build_short_answers(md_text: str) -> str:
    """Turn the '**Qn. ...**' + model-answer pairs into reveal blocks (already HTML)."""
    out = []
    for chunk in re.split(r"\n(?=\*\*Q\d+\.)", md_text):
        chunk = chunk.strip()
        if not chunk:
            continue
        m = re.match(r"\*\*(Q\d+)\.\s*(.+?)\*\*\s*\n(.+)", chunk, re.S)
        if not m:
            out.append(md(chunk))
            continue
        num, question, answer = m.groups()
        out.append(
            f'<div class="sa"><p class="sa__q"><strong><span class="qnum">{num}.</span> '
            f"{md_inline(question)}</strong></p>"
            f'<details class="reveal"><summary>Model answer</summary>'
            f'<div class="reveal__body">{md(answer)}</div></details></div>'
        )
    return "\n".join(out)


def main() -> None:
    raw = SRC.read_text()

    # Drop the markdown title block and the hand-written TOC; the page has its own.
    body_start = raw.index("## 1. The 60-Second Cram Sheet")
    body_md = raw[body_start:]

    # Pre-render the two interactive sections and splice them back in as HTML,
    # so python-markdown never has to reason about embedded block-level markup.
    holders: dict[str, str] = {}

    def stash(key: str, html_fragment: str) -> str:
        token = f"\n\nPLACEHOLDER{key}PLACEHOLDER\n\n"
        holders[f"<p>PLACEHOLDER{key}PLACEHOLDER</p>"] = html_fragment
        return token

    # Multiple-choice block -> question line + option row.
    mc_start = body_md.index("**1.** How many IP addresses")
    mc_end = body_md.index("### Answer key")
    body_md = (
        body_md[:mc_start]
        + stash("MULTIPLECHOICE", build_multiple_choice(body_md[mc_start:mc_end]))
        + body_md[mc_end:]
    )

    # Answer key -> hidden behind a reveal.
    key_match = re.search(r"### Answer key\n+(1-C.+?)\n", body_md)
    if key_match:
        body_md = body_md.replace(
            key_match.group(0),
            stash(
                "ANSWERKEY",
                '<details class="reveal"><summary>Answer key — 45 questions</summary>'
                f'<div class="reveal__body"><p class="answer-key">{key_match.group(1).strip()}'
                "</p></div></details>",
            ),
        )

    # Short-answer section -> one reveal per question.
    sa_start = body_md.index("**Q1.")
    sa_end = body_md.index("## 18.")
    sa_md = body_md[sa_start:sa_end]
    body_md = (
        body_md[:sa_start]
        + stash("SHORTANSWERS", build_short_answers(sa_md))
        + body_md[sa_end:]
    )

    body_html = markdown.markdown(
        loosen_lists(body_md), extensions=["tables", "fenced_code", "sane_lists"]
    )

    for token, fragment in holders.items():
        body_html = body_html.replace(token, fragment)

    # Anchor the h2s and collect nav entries.
    nav_items: list[tuple[str, str]] = []

    def anchor_h2(m: re.Match) -> str:
        inner = m.group(1)
        label = html.unescape(
            re.sub(r"^\d+\.\s*", "", re.sub(r"<[^>]+>", "", inner))
        ).strip()
        slug = slugify(label)
        nav_items.append((slug, label))
        return f'<h2 id="{slug}">{inner}</h2>'

    body_html = re.sub(r"<h2>(.+?)</h2>", anchor_h2, body_html)
    body_html = re.sub(
        r"<h3>(.+?)</h3>",
        lambda m: f'<h3 id="{slugify(m.group(1))}">{m.group(1)}</h3>',
        body_html,
    )

    # Wrap tables so wide content scrolls inside its own container.
    body_html = re.sub(
        r"<table>(.*?)</table>",
        lambda m: f'<div class="table-scroll"><table>{m.group(1)}</table></div>',
        body_html,
        flags=re.S,
    )

    nav = "\n".join(
        f'<li><a href="#{slug}">{html.escape(label)}</a></li>' for slug, label in nav_items
    )

    page = f"""<title>MST400 Final Exam Study Guide</title>
<style>{STYLE}</style>

<a class="skip" href="#main">Skip to content</a>

<div class="shell">
  <aside class="rail">
    <p class="rail__brand">MST400 · Final</p>
    <p class="rail__title">Microsoft Cloud Administration — exam study guide</p>
    <nav aria-label="Sections">
      <ol>
{nav}
      </ol>
    </nav>
  </aside>

  <main class="main" id="main">
    <header class="masthead">
      <p class="masthead__eyebrow">Thursday, August 13 · Room C2032</p>
      <h1>Everything on the MST400 final, in one pass</h1>
      <p>Built from all eleven lecture modules and Labs 01–08. The cram sheet holds the
        numbers that get tested; the module notes explain them; the last two sections let
        you check whether any of it stuck.</p>
      <dl class="facts">
        <div><dt>Questions</dt><dd>29</dd></div>
        <div><dt>Duration</dt><dd>80 min</dd></div>
        <div><dt>Pace</dt><dd>~2.75 min each</dd></div>
        <div><dt>Format</dt><dd>MC + short answer</dd></div>
        <div><dt>Materials</dt><dd>Closed book</dd></div>
      </dl>
    </header>

    <div class="prose">
{body_html}
    </div>
  </main>
</div>

<button class="themer" type="button" aria-label="Cycle colour theme">
  theme <span>system</span>
</button>

<script>{SCRIPT}</script>
"""

    OUT.write_text(page)
    print(f"wrote {OUT} ({len(page):,} bytes, {len(nav_items)} sections)")


if __name__ == "__main__":
    main()
