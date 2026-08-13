/**
 * Regression tests for mst400-practice-exam.html.
 *
 * Runs the page inside a sandboxed iframe WITHOUT allow-modals, which is how
 * the published artifact actually renders. Testing the page standalone hides
 * real bugs: window.confirm() is silently ignored in the artifact sandbox and
 * returns false, which once made both End test buttons dead.
 *
 *   node study-guide/test-exam.mjs
 */

import { chromium } from 'playwright';
import fs from 'fs';
import os from 'os';
import path from 'path';

const PAGE = new URL('./mst400-practice-exam.html', import.meta.url).pathname;
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'mst400-'));

const inner = path.join(tmp, 'inner.html');
const host = path.join(tmp, 'host.html');
fs.writeFileSync(
  inner,
  `<!doctype html><html><head><meta charset="utf-8">` +
    `<meta name="viewport" content="width=device-width,initial-scale=1"></head>` +
    `<body>${fs.readFileSync(PAGE, 'utf8')}</body></html>`
);
fs.writeFileSync(
  host,
  `<!doctype html><html><body style="margin:0"><iframe src="file://${inner}" ` +
    `sandbox="allow-scripts allow-same-origin" style="width:100vw;height:100vh;border:0">` +
    `</iframe></body></html>`
);

let failures = 0;
const check = (name, pass, detail = '') => {
  if (!pass) failures++;
  console.log(`${pass ? 'PASS' : 'FAIL'}  ${name}${detail ? '  — ' + detail : ''}`);
};

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });

async function open({ width = 1100, height = 950, colorScheme = 'light' } = {}) {
  const page = await browser.newPage({ viewport: { width, height }, colorScheme });
  const noise = [];
  page.on('pageerror', (e) => noise.push('pageerror: ' + e.message));
  page.on('console', (m) => {
    if (m.type() === 'error' || /Ignored call/i.test(m.text())) noise.push(m.text());
  });
  // A native dialog would mean the page is still relying on window.confirm.
  page.on('dialog', (d) => { noise.push('native dialog: ' + d.message()); d.dismiss(); });
  await page.goto('file://' + host, { waitUntil: 'load' });
  await page.waitForTimeout(400);
  const frame = page.frames().find((f) => f.url().includes('inner.html'));
  return { page, frame, noise };
}

const screen = (f) =>
  f.evaluate(() => [...document.querySelectorAll('.screen')].find((s) => s.classList.contains('is-active')).id);
const hidden = (f, sel) => f.evaluate((s) => document.querySelector(s).hidden, sel);

/** Answer the current question; returns 'mc' | 'sa'. */
async function answerCurrent(page, frame, optIndex = 0) {
  if (await frame.$('#sa')) {
    await frame.fill('#sa', 'A tenant is the identity boundary; a subscription is the billing unit.');
    if (await frame.$('#check')) {
      await frame.click('#check');
      await page.waitForTimeout(80);
      await frame.click('#sagrade button[data-g="got"]');
    }
    return 'sa';
  }
  if (await frame.$('#qcard .opt:not([disabled])')) {
    const opts = await frame.$$('#qcard .opt');
    await opts[optIndex % opts.length].click();
    await page.waitForTimeout(80);
  }
  return 'mc';
}

/** Advance until a multiple-choice question is on screen. */
async function seekMC(page, frame) {
  const total = parseInt((await frame.textContent('#counter')).split('/')[1], 10);
  for (let i = 0; i < total; i++) {
    if (!(await frame.$('#sa'))) return true;
    await frame.click('#next');
    await page.waitForTimeout(60);
  }
  return false;
}

// ---------------------------------------------------------------- end test
{
  const { page, frame, noise } = await open();
  await frame.click('.mode[data-mode="quick"]');
  await frame.click('#start');
  await page.waitForTimeout(200);
  await answerCurrent(page, frame);

  await frame.click('#endTest');
  await page.waitForTimeout(200);
  check('nav-row End test opens the in-page dialog', !(await hidden(frame, '#confirmEnd')));
  check(
    'dialog states the unanswered count',
    /\d+ questions? (is|are) still unanswered/.test(await frame.textContent('#confirmMsg')),
    (await frame.textContent('#confirmMsg')).trim()
  );

  await frame.click('#confirmNo');
  await page.waitForTimeout(120);
  check('Keep going returns to the test', (await screen(frame)) === 'exam' && (await hidden(frame, '#confirmEnd')));

  await frame.click('#endTest');
  await page.waitForTimeout(120);
  await frame.click('#confirmYes');
  await page.waitForTimeout(250);
  check('Confirm ends the test and shows results', (await screen(frame)) === 'results');

  await frame.click('#retake');
  await frame.click('.mode[data-mode="quick"]');
  await frame.click('#start');
  await page.waitForTimeout(200);
  await frame.click('#submit');
  await page.waitForTimeout(150);
  check('bar End test opens the dialog too', !(await hidden(frame, '#confirmEnd')));

  await page.keyboard.press('Escape');
  await page.waitForTimeout(120);
  check('Escape cancels', (await hidden(frame, '#confirmEnd')) && (await screen(frame)) === 'exam');

  await frame.click('#submit');
  await page.waitForTimeout(120);
  await frame.evaluate(() => document.querySelector('#confirmEnd').click());
  await page.waitForTimeout(120);
  check('backdrop click cancels', await hidden(frame, '#confirmEnd'));

  const total = parseInt((await frame.textContent('#counter')).split('/')[1], 10);
  for (let i = 0; i < total; i++) {
    if (i > 0) { await frame.click('#next'); await page.waitForTimeout(50); }
    await answerCurrent(page, frame);
  }
  await frame.click('#endTest');
  await page.waitForTimeout(250);
  check(
    'fully answered ends with no dialog',
    (await screen(frame)) === 'results' && (await hidden(frame, '#confirmEnd'))
  );

  check('no page errors or ignored modal calls', noise.length === 0, noise.join(' | '));
  await page.close();
}

// ------------------------------------------------------- immediate marking
{
  const { page, frame, noise } = await open();
  await frame.click('.mode[data-mode="quick"]');
  await frame.click('#start');
  await page.waitForTimeout(200);
  check('explanation hidden before answering', !(await frame.$('.explain')));

  await seekMC(page, frame);
  await answerCurrent(page, frame);
  check('explanation shown after answering', !!(await frame.$('.explain')));
  check('exactly one option marked correct', (await frame.$$('.opt.is-right')).length === 1);
  check('options lock after answering', await frame.$eval('#qcard .opt', (e) => e.disabled));
  check('running score appears', !(await hidden(frame, '#runningScore')));
  check(
    'navigator square is colour-coded',
    /is-(ok|no)/.test(await frame.$eval('.dot.is-current', (e) => e.className))
  );
  check('no page errors', noise.length === 0, noise.join(' | '));
  await page.close();
}

// ------------------------------------------------------- grade-at-the-end
{
  const { page, frame, noise } = await open();
  await frame.click('.mode[data-mode="quick"]');
  await frame.click('.mode[data-fb="end"]');
  await frame.click('#start');
  await page.waitForTimeout(200);
  await seekMC(page, frame);
  await answerCurrent(page, frame);
  check('end mode leaks no explanation', !(await frame.$('.explain')));
  check('end mode marks nothing correct', (await frame.$$('.opt.is-right')).length === 0);
  check('end mode keeps options changeable', !(await frame.$eval('#qcard .opt', (e) => e.disabled)));
  check('end mode hides the running score', await hidden(frame, '#runningScore'));
  check('no page errors', noise.length === 0, noise.join(' | '));
  await page.close();
}

// -------------------------------------------------- short-answer marking
{
  const { page, frame, noise } = await open();
  const bank = await frame.evaluate(() => window.__BANK__);
  const byScenario = (sc) => bank.find((q) => q.scenario === sc) || {};
  const saModules = [...new Set(bank.filter((q) => q.type === 'sa').map((q) => q.module))];

  // Walk every module that owns a short answer, feeding it a known input.
  async function sweep(makeAnswer) {
    const seen = new Map();
    for (const m of saModules) {
      await frame.click('.mode[data-mode="focus"]');
      await frame.click(`.chip[data-mod="${m}"]`);
      await frame.click('#start');
      await page.waitForTimeout(120);
      const total = parseInt((await frame.textContent('#counter')).split('/')[1], 10);
      for (let i = 0; i < total; i++) {
        if (i > 0) { await frame.click('#next'); await page.waitForTimeout(45); }
        if (!(await frame.$('#sa'))) continue;
        const q = byScenario(await frame.textContent('.scenario p'));
        if (seen.has(q.id)) continue;
        await frame.fill('#sa', makeAnswer(q));
        await frame.click('#check');
        await page.waitForTimeout(70);
        seen.set(q.id, (await frame.textContent('.verdictline')).trim());
      }
      await frame.click('#endTest');
      await page.waitForTimeout(120);
      if (!(await hidden(frame, '#confirmEnd'))) { await frame.click('#confirmYes'); await page.waitForTimeout(150); }
      await frame.click('#retake');
      await frame.click(`.chip[data-mod="${m}"]`); // deselect for the next module
    }
    return seen;
  }

  const perfect = await sweep((q) => q.model);
  check(
    'model answer scores full marks on every short answer',
    perfect.size > 0 && [...perfect.values()].every((v) => v.startsWith('✓') && v.includes('100%')),
    [...perfect.entries()].filter(([, v]) => !v.includes('100%')).map(([k, v]) => k + ' ' + v).join('; ') || `${perfect.size} checked`
  );

  const junk = await sweep(() => 'The cloud is a computer somewhere else and Azure runs it.');
  check(
    'irrelevant answer scores zero on every short answer',
    junk.size > 0 && [...junk.values()].every((v) => v.startsWith('✗')),
    [...junk.entries()].filter(([, v]) => !v.startsWith('✗')).map(([k, v]) => k + ' ' + v).join('; ') || `${junk.size} checked`
  );

  check('no page errors while marking', noise.length === 0, noise.join(' | '));
  await page.close();
}

// ------------------------------------------------------------------ clock
{
  const { page, frame } = await open();
  await frame.click('.mode[data-mode="quick"]');
  await frame.click('#start');
  await page.waitForTimeout(150);
  check('quick drill is untimed', await hidden(frame, '#clock'));
  await frame.click('#endTest');
  await page.waitForTimeout(120);
  if (!(await hidden(frame, '#confirmEnd'))) await frame.click('#confirmYes');
  await page.waitForTimeout(200);
  // The previously chosen mode stays selected after a retake, so pick full mock explicitly.
  await frame.click('#retake');
  await frame.click('.mode[data-mode="full"]');
  await frame.click('#start');
  await page.waitForTimeout(150);
  check('full mock shows an 80 minute clock', !(await hidden(frame, '#clock')));
  const clockVal = await frame.textContent('#clockVal');
  check('clock counts down from 80:00', /^(80:00|79:5\d)$/.test(clockVal.trim()), clockVal.trim());
  const counter = await frame.textContent('#counter');
  check('full mock draws 29 questions', counter.trim().endsWith('/ 29'), counter.trim());
  await page.close();
}

// -------------------------------------------------- option shuffle fairness
{
  const { page, frame } = await open();
  const scores = [];
  const positions = { A: 0, B: 0, C: 0, D: 0 };
  for (let round = 0; round < 8; round++) {
    if (round > 0) await frame.click('#retake');
    await frame.click('.mode[data-mode="quick"]');
    await frame.click('#start');
    await page.waitForTimeout(120);
    const total = parseInt((await frame.textContent('#counter')).split('/')[1], 10);
    for (let i = 0; i < total; i++) {
      if (i > 0) { await frame.click('#next'); await page.waitForTimeout(40); }
      await answerCurrent(page, frame, 0); // always option A
    }
    await frame.click('#endTest');
    await page.waitForTimeout(200);
    if (!(await hidden(frame, '#confirmEnd'))) { await frame.click('#confirmYes'); await page.waitForTimeout(200); }
    scores.push(parseInt(await frame.textContent('#scoreNum'), 10));
    for (const L of await frame.evaluate(() =>
      [...document.querySelectorAll('.rev .opt.is-right em')].map((e) => e.textContent)
    )) positions[L] = (positions[L] || 0) + 1;
  }
  const avg = scores.reduce((a, c) => a + c, 0) / scores.length;
  check('always picking A scores near chance', avg < 45, `avg ${avg.toFixed(1)}%`);
  check(
    'correct answers land in all four positions',
    Object.values(positions).every((v) => v > 0),
    JSON.stringify(positions)
  );
  await page.close();
}

// --------------------------------------------------------------- rendering
for (const [w, cs] of [[1100, 'dark'], [390, 'dark'], [390, 'light']]) {
  const { page, frame } = await open({ width: w, colorScheme: cs });
  await frame.click('.mode[data-mode="quick"]');
  await frame.click('#start');
  await page.waitForTimeout(150);
  await frame.click('#endTest');
  await page.waitForTimeout(200);
  const over = await frame.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth
  );
  check(`${w}px ${cs}: dialog visible, no horizontal overflow`, !(await hidden(frame, '#confirmEnd')) && over === 0,
    `overflow ${over}px`);
  await page.close();
}

await browser.close();
fs.rmSync(tmp, { recursive: true, force: true });

console.log(failures === 0 ? '\nAll checks passed.' : `\n${failures} check(s) FAILED.`);
process.exit(failures === 0 ? 0 : 1);
