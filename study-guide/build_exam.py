#!/usr/bin/env python3
"""Build the MST400 interactive practice exam page from the question banks."""

import json
from pathlib import Path

HERE = Path(__file__).parent
BANKS = ["bank-a.json", "bank-b.json", "bank-c.json"]
OUT = HERE / "mst400-practice-exam.html"

GUIDE_URL = "https://claude.ai/code/artifact/21b14a1c-59f3-472f-a832-1356ef344e92"

MODULES = [
    ("M1", "Users, Groups & Identities"),
    ("M2", "Governance & Cost"),
    ("M3", "Azure Administration"),
    ("M4", "Virtual Networking"),
    ("M5", "Intersite Connectivity"),
    ("M6", "Traffic Management"),
    ("M7", "Azure Storage"),
    ("M8", "Virtual Machines"),
    ("M9", "App Service & Containers"),
    ("M10", "Data Protection"),
    ("M11", "Monitoring"),
    ("Labs", "Lab Practicals"),
]

STYLE = """
:root {
  color-scheme: light dark;

  --ground:  #f3f6f6;
  --surface: #ffffff;
  --sunken:  #e9eff0;
  --ink:     #131a1c;
  --muted:   #55666a;
  --faint:   #7c8e91;
  --rule:    #d7e0e0;
  --rule-soft: #e6eded;
  --accent:  #0e6e75;
  --accent-soft: #dcedee;
  --good:    #14663f;
  --good-soft: #dcefe3;
  --bad:     #9c3418;
  --bad-soft: #f8e4dd;
  --warn:    #8a5300;
  --warn-soft: #fbedd6;

  --font-display: Georgia, "Iowan Old Style", "Source Serif 4", "Times New Roman", serif;
  --font-body: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
  --font-mono: ui-monospace, "SF Mono", "Cascadia Mono", Menlo, Consolas, monospace;
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --ground:  #0e1416;
    --surface: #151d20;
    --sunken:  #1c2528;
    --ink:     #e3eaea;
    --muted:   #93a4a6;
    --faint:   #74868a;
    --rule:    #253133;
    --rule-soft: #1e282b;
    --accent:  #4ec3ca;
    --accent-soft: #10393c;
    --good:    #5fc98f;
    --good-soft: #123326;
    --bad:     #f0907a;
    --bad-soft: #3a1f18;
    --warn:    #e2b264;
    --warn-soft: #33270f;
  }
}

:root[data-theme="dark"] {
  --ground:  #0e1416;
  --surface: #151d20;
  --sunken:  #1c2528;
  --ink:     #e3eaea;
  --muted:   #93a4a6;
  --faint:   #74868a;
  --rule:    #253133;
  --rule-soft: #1e282b;
  --accent:  #4ec3ca;
  --accent-soft: #10393c;
  --good:    #5fc98f;
  --good-soft: #123326;
  --bad:     #f0907a;
  --bad-soft: #3a1f18;
  --warn:    #e2b264;
  --warn-soft: #33270f;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--ground);
  color: var(--ink);
  font-family: var(--font-body);
  font-size: 16px;
  line-height: 1.6;
  -webkit-text-size-adjust: 100%;
}

.page { max-width: 54rem; margin: 0 auto; padding: 0 1.5rem 6rem; }

.eyebrow {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--accent);
  margin: 0 0 0.7rem;
}

h1 {
  font-family: var(--font-display);
  font-size: clamp(1.9rem, 4vw, 2.7rem);
  line-height: 1.1;
  letter-spacing: -0.015em;
  font-weight: 600;
  margin: 0 0 0.9rem;
  text-wrap: balance;
}

h2 {
  font-family: var(--font-display);
  font-size: 1.4rem;
  font-weight: 600;
  margin: 0 0 0.9rem;
  text-wrap: balance;
}

h3 {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.13em;
  text-transform: uppercase;
  color: var(--faint);
  font-weight: 600;
  margin: 0 0 0.7rem;
}

p { margin: 0 0 1rem; }
.lede { color: var(--muted); max-width: 46ch; }

.screen { display: none; }
.screen.is-active { display: block; }

/* ---------- setup ---------- */

.setup-head { padding: 4rem 0 2rem; border-bottom: 2px solid var(--ink); margin-bottom: 2.25rem; }

.modes {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr));
  gap: 0.9rem;
  margin: 0 0 2rem;
}

.mode {
  text-align: left;
  background: var(--surface);
  border: 1px solid var(--rule);
  border-left: 3px solid var(--rule);
  padding: 1.1rem 1.2rem;
  cursor: pointer;
  font: inherit;
  color: inherit;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.mode:hover { border-color: var(--accent); }

.mode[aria-pressed="true"] {
  border-color: var(--accent);
  border-left-color: var(--accent);
  background: var(--accent-soft);
}

.mode b { font-size: 1.02rem; font-weight: 650; }
.mode small { color: var(--muted); font-size: 0.87rem; line-height: 1.45; }

.mode .spec {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--accent);
}

.cross {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin-top: 2.5rem;
  padding: 0.85rem 1.1rem;
  background: var(--surface);
  border: 1px solid var(--rule);
  border-left: 3px solid var(--accent);
  font-size: 0.93rem;
}

.cross a {
  color: var(--accent);
  font-weight: 600;
  text-decoration: none;
  border-bottom: 1px solid color-mix(in srgb, var(--accent) 40%, transparent);
}
.cross a:hover { border-bottom-color: var(--accent); }
.cross span { color: var(--muted); }

.picker { margin: 0 0 2rem; }
.picker[hidden] { display: none; }

.chips { display: flex; flex-wrap: wrap; gap: 0.45rem; margin-bottom: 0.8rem; }

.chip {
  font: inherit;
  font-size: 0.85rem;
  cursor: pointer;
  background: var(--surface);
  color: var(--muted);
  border: 1px solid var(--rule);
  border-radius: 999px;
  padding: 0.35rem 0.85rem;
  display: inline-flex;
  gap: 0.45rem;
  align-items: baseline;
}

.chip:hover { border-color: var(--accent); color: var(--ink); }

.chip[aria-pressed="true"] {
  background: var(--accent-soft);
  border-color: var(--accent);
  color: var(--ink);
  font-weight: 600;
}

.chip i {
  font-style: normal;
  font-family: var(--font-mono);
  font-size: 0.72em;
  color: var(--faint);
}

.btn {
  font: inherit;
  font-weight: 600;
  cursor: pointer;
  border: 1px solid var(--accent);
  background: var(--accent);
  color: var(--ground);
  padding: 0.7rem 1.4rem;
  border-radius: 2px;
}

.btn:hover { filter: brightness(1.08); }
.btn:disabled { opacity: 0.45; cursor: not-allowed; }

.btn--ghost {
  background: transparent;
  color: var(--accent);
}

.btn--quiet {
  background: var(--surface);
  border-color: var(--rule);
  color: var(--muted);
  font-weight: 500;
}
.btn--quiet:hover { color: var(--ink); border-color: var(--accent); }

.btn--sm { padding: 0.4rem 0.85rem; font-size: 0.85rem; }

/* ---------- exam bar ---------- */

.bar {
  position: sticky;
  top: 0;
  z-index: 10;
  background: var(--ground);
  border-bottom: 1px solid var(--rule);
  padding: 0.85rem 0;
  margin-bottom: 1.75rem;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  flex-wrap: wrap;
}

.bar__stat {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--faint);
  display: flex;
  align-items: baseline;
  gap: 0.45rem;
}

.bar__stat b {
  font-size: 1.05rem;
  letter-spacing: 0;
  color: var(--ink);
  font-variant-numeric: tabular-nums;
}

#clock.is-warn b { color: var(--warn); }
#clock.is-crit b { color: var(--bad); }

.bar__spacer { flex: 1; }

.meter {
  flex-basis: 100%;
  height: 3px;
  background: var(--rule);
  overflow: hidden;
}
.meter span { display: block; height: 100%; background: var(--accent); width: 0; transition: width 0.2s; }
@media (prefers-reduced-motion: reduce) { .meter span { transition: none; } }

/* ---------- question card ---------- */

.qcard {
  background: var(--surface);
  border: 1px solid var(--rule);
  padding: 1.5rem 1.6rem 1.6rem;
  margin-bottom: 1.25rem;
}

.qmeta {
  display: flex;
  align-items: baseline;
  gap: 0.8rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}

.tag {
  font-family: var(--font-mono);
  font-size: 0.66rem;
  letter-spacing: 0.11em;
  text-transform: uppercase;
  padding: 0.2rem 0.5rem;
  border: 1px solid var(--rule);
  color: var(--muted);
}

.tag--type { color: var(--accent); border-color: var(--accent); }

.scenario {
  background: var(--sunken);
  border-left: 3px solid var(--accent);
  padding: 0.9rem 1.1rem;
  margin: 0 0 1.15rem;
  font-size: 0.96rem;
}
.scenario p { margin: 0; }

.qtext { font-size: 1.08rem; font-weight: 650; margin: 0 0 1.1rem; text-wrap: balance; }

.opts { display: flex; flex-direction: column; gap: 0.5rem; }

.opt {
  display: grid;
  grid-template-columns: 1.6rem 1fr;
  gap: 0.6rem;
  align-items: start;
  text-align: left;
  font: inherit;
  cursor: pointer;
  background: var(--surface);
  color: inherit;
  border: 1px solid var(--rule);
  padding: 0.7rem 0.9rem;
  line-height: 1.5;
}

.opt:hover { border-color: var(--accent); }

.opt em {
  font-style: normal;
  font-family: var(--font-mono);
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--faint);
  padding-top: 0.12rem;
}

.opt[aria-pressed="true"] {
  border-color: var(--accent);
  background: var(--accent-soft);
}
.opt[aria-pressed="true"] em { color: var(--accent); }

.opt.is-right { border-color: var(--good); background: var(--good-soft); }
.opt.is-right em { color: var(--good); }
.opt.is-wrong { border-color: var(--bad); background: var(--bad-soft); }
.opt.is-wrong em { color: var(--bad); }
.opt[disabled] { cursor: default; }

textarea {
  width: 100%;
  min-height: 9rem;
  font: inherit;
  font-size: 0.96rem;
  line-height: 1.6;
  padding: 0.8rem 0.9rem;
  background: var(--sunken);
  color: var(--ink);
  border: 1px solid var(--rule);
  resize: vertical;
}
textarea:focus { border-color: var(--accent); }

.hint {
  font-size: 0.85rem;
  color: var(--faint);
  margin: 0.6rem 0 0;
}

.nav-row { display: flex; gap: 0.6rem; align-items: center; flex-wrap: wrap; }
.nav-row .grow { flex: 1; }

/* ---------- navigator ---------- */

.navigator { margin-top: 2rem; padding-top: 1.4rem; border-top: 1px solid var(--rule); }

.dots { display: flex; flex-wrap: wrap; gap: 0.3rem; }

.dot {
  width: 2rem;
  height: 2rem;
  font: inherit;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  cursor: pointer;
  background: var(--surface);
  color: var(--faint);
  border: 1px solid var(--rule);
  position: relative;
  padding: 0;
}

.dot:hover { border-color: var(--accent); color: var(--ink); }
.dot.is-answered { background: var(--sunken); color: var(--ink); border-color: var(--rule); }
.dot.is-current { border-color: var(--accent); color: var(--accent); font-weight: 700; box-shadow: inset 0 0 0 1px var(--accent); }
.dot.is-flagged::after {
  content: "";
  position: absolute;
  top: 2px; right: 2px;
  width: 5px; height: 5px;
  border-radius: 50%;
  background: var(--warn);
}

.legend {
  display: flex;
  gap: 1.1rem;
  flex-wrap: wrap;
  margin-top: 0.9rem;
  font-family: var(--font-mono);
  font-size: 0.66rem;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: var(--faint);
}
.legend span { display: inline-flex; align-items: center; gap: 0.35rem; }
.legend i { width: 0.7rem; height: 0.7rem; border: 1px solid var(--rule); font-style: normal; }
.legend i.f { background: var(--sunken); }
.legend i.g { border-color: var(--accent); }
.legend i.w { background: var(--warn); border-color: var(--warn); border-radius: 50%; }

/* ---------- results ---------- */

.scoreline {
  display: flex;
  align-items: baseline;
  gap: 1.4rem;
  flex-wrap: wrap;
  padding: 2.5rem 0 1.5rem;
  border-bottom: 2px solid var(--ink);
  margin-bottom: 2rem;
}

.bigscore {
  font-family: var(--font-display);
  font-size: clamp(3rem, 9vw, 4.6rem);
  line-height: 0.95;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}
.bigscore small { font-size: 0.32em; color: var(--muted); font-weight: 400; }

.verdict { font-size: 1rem; color: var(--muted); max-width: 34ch; }

.bars { display: flex; flex-direction: column; gap: 0.55rem; margin: 0 0 2.25rem; }

.brow {
  display: grid;
  grid-template-columns: minmax(8rem, 12rem) 1fr 3.6rem;
  gap: 0.8rem;
  align-items: center;
  font-size: 0.89rem;
}

.brow .name { color: var(--muted); }
.brow .track {
  display: block;
  height: 0.75rem;
  background: var(--rule-soft);
  border: 1px solid var(--rule);
  overflow: hidden;
}
.brow .fill { display: block; height: 100%; background: var(--accent); min-width: 2px; }
.brow .fill.low { background: var(--bad); }
.brow .fill.mid { background: var(--warn); }
.brow .val { font-family: var(--font-mono); font-size: 0.8rem; text-align: right; font-variant-numeric: tabular-nums; color: var(--muted); }

.callout {
  border: 1px solid var(--rule);
  border-left: 3px solid var(--warn);
  background: var(--warn-soft);
  padding: 1rem 1.15rem;
  margin: 0 0 2.25rem;
  font-size: 0.95rem;
}
.callout h3 { color: var(--warn); margin-bottom: 0.45rem; }
.callout p:last-child { margin-bottom: 0; }
.callout a { color: var(--ink); }

.review { display: flex; flex-direction: column; gap: 0.7rem; }

.rev {
  border: 1px solid var(--rule);
  border-left: 3px solid var(--rule);
  background: var(--surface);
}
.rev.ok { border-left-color: var(--good); }
.rev.no { border-left-color: var(--bad); }
.rev.part { border-left-color: var(--warn); }

.rev > summary {
  cursor: pointer;
  list-style: none;
  padding: 0.75rem 1rem;
  display: grid;
  grid-template-columns: 2rem 1fr auto;
  gap: 0.7rem;
  align-items: baseline;
  font-size: 0.94rem;
}
.rev > summary::-webkit-details-marker { display: none; }
.rev > summary:hover { background: var(--sunken); }
.rev > summary .n { font-family: var(--font-mono); font-size: 0.78rem; color: var(--faint); }
.rev > summary .mark { font-family: var(--font-mono); font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; }
.rev.ok .mark { color: var(--good); }
.rev.no .mark { color: var(--bad); }
.rev.part .mark { color: var(--warn); }

.rev__body { padding: 0.4rem 1rem 1.1rem; border-top: 1px solid var(--rule-soft); }

.explain {
  background: var(--sunken);
  border-left: 3px solid var(--accent);
  padding: 0.85rem 1rem;
  margin: 0.9rem 0 0;
  font-size: 0.93rem;
}
.explain strong { color: var(--accent); }

.model { font-size: 0.94rem; }
.yours {
  white-space: pre-wrap;
  background: var(--sunken);
  border: 1px solid var(--rule);
  padding: 0.75rem 0.9rem;
  font-size: 0.92rem;
  margin: 0 0 1rem;
}
.yours:empty::before { content: "(left blank)"; color: var(--faint); }

.terms { display: flex; flex-wrap: wrap; gap: 0.35rem; margin: 0.7rem 0 0; }
.terms b {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 500;
  padding: 0.18rem 0.5rem;
  border: 1px solid var(--rule);
  color: var(--muted);
}
.terms b.hit { border-color: var(--good); color: var(--good); background: var(--good-soft); }

.grade { display: flex; gap: 0.5rem; flex-wrap: wrap; margin: 1rem 0 0; }
.grade button[aria-pressed="true"] { background: var(--accent); color: var(--ground); border-color: var(--accent); }

.themer {
  position: fixed;
  right: 1.1rem;
  bottom: 1.1rem;
  z-index: 20;
  display: flex;
  gap: 0.4rem;
  padding: 0.45rem 0.75rem;
  background: var(--surface);
  border: 1px solid var(--rule);
  border-radius: 999px;
  color: var(--muted);
  font-family: var(--font-mono);
  font-size: 0.66rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  cursor: pointer;
}
.themer:hover { color: var(--ink); border-color: var(--accent); }

:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }

@media (max-width: 40rem) {
  .qcard { padding: 1.15rem 1.1rem 1.25rem; }
  .brow { grid-template-columns: 1fr; gap: 0.25rem; }
  .brow .val { text-align: left; }
}

@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; }
}
"""

SCRIPT = r"""
(function () {
  'use strict';

  var BANK = window.__BANK__;
  var MODULES = window.__MODULES__;
  var GUIDE = window.__GUIDE__;
  var MODNAME = {};
  MODULES.forEach(function (m) { MODNAME[m[0]] = m[1]; });

  var $ = function (s) { return document.querySelector(s); };

  // ---------- theme ----------
  var root = document.documentElement;
  var themer = $('.themer');
  var themes = ['system', 'light', 'dark'];
  var themeIx = 0;
  themer.addEventListener('click', function () {
    themeIx = (themeIx + 1) % themes.length;
    var t = themes[themeIx];
    if (t === 'system') root.removeAttribute('data-theme');
    else root.setAttribute('data-theme', t);
    themer.querySelector('span').textContent = t;
  });

  // ---------- helpers ----------
  function shuffle(a) {
    var out = a.slice();
    for (var i = out.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = out[i]; out[i] = out[j]; out[j] = t;
    }
    return out;
  }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function show(id) {
    ['setup', 'exam', 'results'].forEach(function (s) {
      $('#' + s).classList.toggle('is-active', s === id);
    });
    window.scrollTo(0, 0);
  }

  // ---------- setup ----------
  var MODES = {
    full:   { label: 'Full mock exam', count: 29, sa: 4, minutes: 80 },
    quick:  { label: 'Quick drill',    count: 10, sa: 1, minutes: 0  },
    focus:  { label: 'Module focus',   count: 15, sa: 2, minutes: 0  }
  };
  var mode = 'full';
  var picked = {};

  Array.prototype.forEach.call(document.querySelectorAll('.mode'), function (b) {
    b.addEventListener('click', function () {
      mode = b.dataset.mode;
      Array.prototype.forEach.call(document.querySelectorAll('.mode'), function (o) {
        o.setAttribute('aria-pressed', String(o === b));
      });
      $('#picker').hidden = mode !== 'focus';
      syncStart();
    });
  });

  Array.prototype.forEach.call(document.querySelectorAll('.chip'), function (c) {
    c.addEventListener('click', function () {
      var on = c.getAttribute('aria-pressed') === 'true';
      c.setAttribute('aria-pressed', String(!on));
      picked[c.dataset.mod] = !on;
      syncStart();
    });
  });

  function chosenModules() {
    return Object.keys(picked).filter(function (k) { return picked[k]; });
  }

  function syncStart() {
    var ok = mode !== 'focus' || chosenModules().length > 0;
    $('#start').disabled = !ok;
    $('#startNote').textContent = ok
      ? (mode === 'focus'
          ? chosenModules().length + ' module(s) selected'
          : MODES[mode].count + ' questions' + (MODES[mode].minutes ? ' · ' + MODES[mode].minutes + ' minutes' : ' · untimed'))
      : 'Select at least one module';
  }

  // ---------- exam state ----------
  var paper = [];
  var cur = 0;
  var deadline = 0;
  var ticker = null;

  function draw() {
    var cfg = MODES[mode];
    var pool = BANK.filter(function (q) {
      return mode !== 'focus' || picked[q.module];
    });
    var mcPool = shuffle(pool.filter(function (q) { return q.type === 'mc'; }));
    var saPool = shuffle(pool.filter(function (q) { return q.type === 'sa'; }));

    var wantSA = Math.min(cfg.sa, saPool.length);
    var wantMC = Math.min(cfg.count - wantSA, mcPool.length);
    var picks = mcPool.slice(0, wantMC).concat(saPool.slice(0, wantSA));

    paper = shuffle(picks).map(function (q) {
      var item = { q: q, flagged: false, chosen: null, text: '', grade: null };
      if (q.type === 'mc') {
        var order = shuffle(q.options.map(function (_, i) { return i; }));
        item.order = order;
        item.correct = order.indexOf(0);
      }
      return item;
    });
    cur = 0;
  }

  function startExam() {
    draw();
    var mins = MODES[mode].minutes;
    if (mins) {
      deadline = Date.now() + mins * 60000;
      $('#clock').hidden = false;
      ticker = setInterval(tick, 1000);
      tick();
    } else {
      $('#clock').hidden = true;
    }
    show('exam');
    renderQuestion();
    renderDots();
  }

  function tick() {
    var left = Math.max(0, deadline - Date.now());
    var m = Math.floor(left / 60000);
    var s = Math.floor((left % 60000) / 1000);
    $('#clockVal').textContent = m + ':' + (s < 10 ? '0' : '') + s;
    var el = $('#clock');
    el.classList.toggle('is-warn', left <= 600000 && left > 120000);
    el.classList.toggle('is-crit', left <= 120000);
    if (left === 0) { clearInterval(ticker); finish(); }
  }

  function answeredCount() {
    return paper.filter(function (it) {
      return it.q.type === 'mc' ? it.chosen !== null : it.text.trim().length > 0;
    }).length;
  }

  function renderQuestion() {
    var it = paper[cur];
    var q = it.q;
    var h = '';

    h += '<div class="qmeta">';
    h += '<span class="tag tag--type">' + (q.type === 'mc' ? 'Multiple choice' : 'Short answer') + '</span>';
    h += '<span class="tag">' + esc(q.module === 'Labs' ? 'Labs' : q.module) + ' · ' + esc(MODNAME[q.module]) + '</span>';
    h += '</div>';

    h += '<div class="scenario"><p>' + esc(q.scenario) + '</p></div>';
    h += '<p class="qtext">' + esc(q.q) + '</p>';

    if (q.type === 'mc') {
      h += '<div class="opts">';
      it.order.forEach(function (srcIx, pos) {
        h += '<button class="opt" type="button" data-pos="' + pos + '" aria-pressed="' +
             (it.chosen === pos) + '"><em>' + 'ABCD'[pos] + '</em><span>' +
             esc(q.options[srcIx]) + '</span></button>';
      });
      h += '</div>';
    } else {
      h += '<textarea id="sa" placeholder="Write your answer. Aim for the key terms — graders scan for them.">' +
           esc(it.text) + '</textarea>';
      h += '<p class="hint">You will grade this yourself against a model answer at the end.</p>';
    }

    $('#qcard').innerHTML = h;
    $('#counter').textContent = (cur + 1) + ' / ' + paper.length;
    $('#progress').style.width = (answeredCount() / paper.length * 100) + '%';
    $('#answered').textContent = answeredCount() + ' / ' + paper.length;
    $('#flag').setAttribute('aria-pressed', String(it.flagged));
    $('#flag').textContent = it.flagged ? 'Unflag' : 'Flag for review';
    $('#prev').disabled = cur === 0;
    $('#next').disabled = cur === paper.length - 1;

    Array.prototype.forEach.call($('#qcard').querySelectorAll('.opt'), function (b) {
      b.addEventListener('click', function () {
        it.chosen = Number(b.dataset.pos);
        renderQuestion();
        renderDots();
      });
    });
    var ta = $('#sa');
    if (ta) {
      ta.addEventListener('input', function () {
        it.text = ta.value;
        $('#progress').style.width = (answeredCount() / paper.length * 100) + '%';
        $('#answered').textContent = answeredCount() + ' / ' + paper.length;
        renderDots();
      });
    }
  }

  function renderDots() {
    var h = '';
    paper.forEach(function (it, i) {
      var done = it.q.type === 'mc' ? it.chosen !== null : it.text.trim().length > 0;
      h += '<button class="dot' + (done ? ' is-answered' : '') +
           (it.flagged ? ' is-flagged' : '') + (i === cur ? ' is-current' : '') +
           '" data-i="' + i + '" type="button" aria-label="Question ' + (i + 1) + '">' + (i + 1) + '</button>';
    });
    $('#dots').innerHTML = h;
    Array.prototype.forEach.call($('#dots').querySelectorAll('.dot'), function (b) {
      b.addEventListener('click', function () {
        cur = Number(b.dataset.i);
        renderQuestion();
        renderDots();
      });
    });
  }

  $('#prev').addEventListener('click', function () { if (cur > 0) { cur--; renderQuestion(); renderDots(); } });
  $('#next').addEventListener('click', function () { if (cur < paper.length - 1) { cur++; renderQuestion(); renderDots(); } });
  $('#flag').addEventListener('click', function () {
    paper[cur].flagged = !paper[cur].flagged;
    renderQuestion();
    renderDots();
  });

  $('#submit').addEventListener('click', function () {
    var left = paper.length - answeredCount();
    if (left > 0 && !confirm(left + ' question(s) are unanswered. Submit anyway?')) return;
    finish();
  });

  $('#start').addEventListener('click', startExam);
  $('#retake').addEventListener('click', function () { show('setup'); });

  // ---------- results ----------
  function finish() {
    if (ticker) { clearInterval(ticker); ticker = null; }
    paper.forEach(function (it) {
      if (it.q.type === 'sa') it.grade = null;
    });
    renderResults();
    show('results');
  }

  function scoreOf(it) {
    if (it.q.type === 'mc') return it.chosen === it.correct ? 1 : 0;
    if (it.grade === 'got') return 1;
    if (it.grade === 'part') return 0.5;
    return 0;
  }

  function renderResults() {
    var mcItems = paper.filter(function (it) { return it.q.type === 'mc'; });
    var total = paper.reduce(function (a, it) { return a + scoreOf(it); }, 0);
    var pct = Math.round(total / paper.length * 100);

    $('#scoreNum').innerHTML = pct + '<small>%</small>';
    $('#scoreSub').textContent = (Math.round(total * 10) / 10) + ' of ' + paper.length +
      ' · ' + mcItems.filter(function (it) { return it.chosen === it.correct; }).length +
      ' of ' + mcItems.length + ' multiple choice correct';

    var ungraded = paper.filter(function (it) { return it.q.type === 'sa' && it.grade === null; }).length;
    $('#verdict').textContent = ungraded
      ? 'Grade your ' + ungraded + ' short answer(s) below and the score will update.'
      : (pct >= 85 ? 'Strong. Draw another paper to confirm it holds across different questions.'
        : pct >= 70 ? 'Solid pass. Work the weakest modules below, then re-draw.'
        : 'Below where you want to be on Thursday. Reread the weak modules before drawing again.');

    // per-module
    var agg = {};
    paper.forEach(function (it) {
      var m = it.q.module;
      if (!agg[m]) agg[m] = { got: 0, of: 0 };
      agg[m].got += scoreOf(it);
      agg[m].of += 1;
    });
    var rows = Object.keys(agg).sort(function (a, b) {
      return (agg[a].got / agg[a].of) - (agg[b].got / agg[b].of);
    });
    var bh = '';
    rows.forEach(function (m) {
      var p = Math.round(agg[m].got / agg[m].of * 100);
      var cls = p < 50 ? 'low' : p < 75 ? 'mid' : '';
      bh += '<div class="brow"><span class="name">' + esc(MODNAME[m]) + '</span>' +
            '<span class="track"><span class="fill ' + cls + '" style="width:' + p + '%"></span></span>' +
            '<span class="val">' + p + '%</span></div>';
    });
    $('#bars').innerHTML = bh;

    var weak = rows.filter(function (m) { return agg[m].got / agg[m].of < 0.75; }).slice(0, 3);
    if (weak.length) {
      $('#weak').hidden = false;
      $('#weakList').innerHTML = 'Reread ' + weak.map(function (m) {
        return '<strong>' + esc(MODNAME[m]) + '</strong>';
      }).join(', ') + ' in the <a href="' + GUIDE + '" target="_blank" rel="noopener">study guide</a>, then draw a fresh paper.';
    } else {
      $('#weak').hidden = true;
    }

    // review
    var rh = '';
    paper.forEach(function (it, i) {
      var q = it.q;
      var cls, mark;
      if (q.type === 'mc') {
        cls = it.chosen === it.correct ? 'ok' : 'no';
        mark = it.chosen === null ? 'Skipped' : (cls === 'ok' ? 'Correct' : 'Incorrect');
        if (it.chosen === null) cls = 'no';
      } else {
        cls = it.grade === 'got' ? 'ok' : it.grade === 'part' ? 'part' : it.grade === 'miss' ? 'no' : '';
        mark = it.grade === null ? 'Grade this' : (it.grade === 'got' ? 'Got it' : it.grade === 'part' ? 'Partial' : 'Missed');
      }

      // Some questions are deliberately terse ("Why?"); the scenario is what identifies them.
      var label = q.q.length < 32
        ? q.scenario.slice(0, 96).replace(/\s+\S*$/, '') + '… ' + q.q
        : q.q;

      rh += '<details class="rev ' + cls + '" data-i="' + i + '"' + (q.type === 'sa' && it.grade === null ? ' open' : '') + '>';
      rh += '<summary><span class="n">' + (i + 1) + '</span><span>' + esc(label) +
            '</span><span class="mark">' + mark + '</span></summary>';
      rh += '<div class="rev__body">';
      rh += '<div class="scenario"><p>' + esc(q.scenario) + '</p></div>';

      if (q.type === 'mc') {
        rh += '<div class="opts">';
        it.order.forEach(function (srcIx, pos) {
          var k = '';
          if (pos === it.correct) k = ' is-right';
          else if (pos === it.chosen) k = ' is-wrong';
          rh += '<button class="opt' + k + '" type="button" disabled><em>' + 'ABCD'[pos] +
                '</em><span>' + esc(q.options[srcIx]) + (pos === it.chosen ? '  ← your answer' : '') +
                '</span></button>';
        });
        rh += '</div>';
        rh += '<div class="explain"><strong>Why:</strong> ' + esc(q.explain) + '</div>';
      } else {
        rh += '<h3>Your answer</h3><div class="yours">' + esc(it.text.trim()) + '</div>';
        rh += '<h3>Model answer</h3><p class="model">' + esc(q.model) + '</p>';
        var lower = it.text.toLowerCase();
        rh += '<h3>Key terms a grader scans for</h3><div class="terms">';
        q.keyTerms.forEach(function (t) {
          var hit = lower.indexOf(t.toLowerCase()) !== -1;
          rh += '<b class="' + (hit ? 'hit' : '') + '">' + esc(t) + '</b>';
        });
        rh += '</div>';
        rh += '<div class="grade" data-grade="' + i + '">' +
              '<button class="btn btn--quiet btn--sm" data-g="got" aria-pressed="' + (it.grade === 'got') + '">Got it</button>' +
              '<button class="btn btn--quiet btn--sm" data-g="part" aria-pressed="' + (it.grade === 'part') + '">Partial</button>' +
              '<button class="btn btn--quiet btn--sm" data-g="miss" aria-pressed="' + (it.grade === 'miss') + '">Missed</button>' +
              '</div>';
      }
      rh += '</div></details>';
    });
    $('#review').innerHTML = rh;

    Array.prototype.forEach.call($('#review').querySelectorAll('.grade button'), function (b) {
      b.addEventListener('click', function () {
        var i = Number(b.parentElement.dataset.grade);
        paper[i].grade = b.dataset.g;
        var open = [];
        Array.prototype.forEach.call($('#review').querySelectorAll('.rev'), function (d) {
          if (d.open) open.push(Number(d.dataset.i));
        });
        renderResults();
        open.forEach(function (ix) {
          var d = $('#review').querySelector('.rev[data-i="' + ix + '"]');
          if (d) d.open = true;
        });
      });
    });
  }

  // keyboard
  document.addEventListener('keydown', function (e) {
    if (!$('#exam').classList.contains('is-active')) return;
    if (e.target.tagName === 'TEXTAREA') return;
    if (e.key === 'ArrowRight') $('#next').click();
    if (e.key === 'ArrowLeft') $('#prev').click();
    var n = 'abcd'.indexOf(e.key.toLowerCase());
    if (n > -1) {
      var b = $('#qcard').querySelector('.opt[data-pos="' + n + '"]');
      if (b) b.click();
    }
  });

  syncStart();
})();
"""


def main() -> None:
    bank = []
    for name in BANKS:
        bank.extend(json.loads((HERE / name).read_text()))

    counts: dict[str, int] = {}
    for q in bank:
        counts[q["module"]] = counts.get(q["module"], 0) + 1

    chips = "\n".join(
        f'<button class="chip" type="button" data-mod="{code}" aria-pressed="false">'
        f"{label} <i>{counts.get(code, 0)}</i></button>"
        for code, label in MODULES
    )

    payload = json.dumps(bank, separators=(",", ":")).replace("</", "<\\/")
    modules_json = json.dumps(MODULES).replace("</", "<\\/")

    page = f"""<title>MST400 Practice Exam</title>
<style>{STYLE}</style>

<div class="page">

  <section id="setup" class="screen is-active">
    <div class="setup-head">
      <p class="eyebrow">MST400 &middot; Practice engine &middot; {len(bank)} questions</p>
      <h1>Draw a practice paper</h1>
      <p class="lede">Every paper is a fresh random draw, and the answer options are reshuffled each
        time, so you cannot memorise position. Questions are scenario-based: you are given a
        situation and asked what you would actually do.</p>
    </div>

    <h2>Choose a paper</h2>
    <div class="modes">
      <button class="mode" type="button" data-mode="full" aria-pressed="true">
        <span class="spec">29 questions &middot; 80 min</span>
        <b>Full mock exam</b>
        <small>Matches Thursday exactly: 29 questions, 25 multiple choice and 4 short answer,
          on an 80-minute countdown that submits automatically.</small>
      </button>
      <button class="mode" type="button" data-mode="quick" aria-pressed="false">
        <span class="spec">10 questions &middot; untimed</span>
        <b>Quick drill</b>
        <small>A short untimed set for a spare fifteen minutes. Mixed modules, mostly
          multiple choice.</small>
      </button>
      <button class="mode" type="button" data-mode="focus" aria-pressed="false">
        <span class="spec">15 questions &middot; untimed</span>
        <b>Module focus</b>
        <small>Drill only the modules you pick. Use this after a full mock shows you where
          the gaps are.</small>
      </button>
    </div>

    <div class="picker" id="picker" hidden>
      <h3>Modules to include</h3>
      <div class="chips">
{chips}
      </div>
    </div>

    <div class="nav-row">
      <button class="btn" id="start" type="button">Start paper</button>
      <span class="hint" id="startNote"></span>
    </div>

    <p class="cross">
      <a href="{GUIDE_URL}" target="_blank" rel="noopener">Study guide &rarr;</a>
      <span>All eleven modules, the lab recap, and the cram sheet of numbers. Read there, then test here.</span>
    </p>
  </section>

  <section id="exam" class="screen">
    <div class="bar">
      <span class="bar__stat" id="clock" hidden>Time left <b id="clockVal">80:00</b></span>
      <span class="bar__stat">Question <b id="counter">1 / 29</b></span>
      <span class="bar__stat">Answered <b id="answered">0 / 29</b></span>
      <span class="bar__spacer"></span>
      <button class="btn btn--sm" id="submit" type="button">Submit paper</button>
      <span class="meter"><span id="progress"></span></span>
    </div>

    <div class="qcard" id="qcard"></div>

    <div class="nav-row">
      <button class="btn btn--quiet" id="prev" type="button">&larr; Previous</button>
      <button class="btn btn--quiet" id="next" type="button">Next &rarr;</button>
      <span class="grow"></span>
      <button class="btn btn--quiet" id="flag" type="button" aria-pressed="false">Flag for review</button>
    </div>

    <div class="navigator">
      <h3>Paper</h3>
      <div class="dots" id="dots"></div>
      <div class="legend">
        <span><i class="f"></i> answered</span>
        <span><i class="g"></i> current</span>
        <span><i class="w"></i> flagged</span>
        <span>keys: A&ndash;D to answer, &larr; &rarr; to move</span>
      </div>
    </div>
  </section>

  <section id="results" class="screen">
    <div class="scoreline">
      <span class="bigscore" id="scoreNum">0<small>%</small></span>
      <span>
        <p class="eyebrow" id="scoreSub"></p>
        <p class="verdict" id="verdict"></p>
      </span>
    </div>

    <h2>By module</h2>
    <div class="bars" id="bars"></div>

    <div class="callout" id="weak" hidden>
      <h3>Where to spend tonight</h3>
      <p id="weakList"></p>
    </div>

    <h2>Review every question</h2>
    <div class="review" id="review"></div>

    <div class="nav-row" style="margin-top:2rem">
      <button class="btn" id="retake" type="button">Draw another paper</button>
      <span class="hint">A new random selection, with options reshuffled again.</span>
    </div>
  </section>

</div>

<button class="themer" type="button" aria-label="Cycle colour theme">theme <span>system</span></button>

<script>
window.__BANK__ = {payload};
window.__MODULES__ = {modules_json};
window.__GUIDE__ = "{GUIDE_URL}";
</script>
<script>{SCRIPT}</script>
"""

    OUT.write_text(page)
    print(f"wrote {OUT} ({len(page):,} bytes, {len(bank)} questions)")


if __name__ == "__main__":
    main()
