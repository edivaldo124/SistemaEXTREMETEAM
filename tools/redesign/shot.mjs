// Capturas isoladas do redesign. Uso: node shot.mjs jobs.json
// jobs: [{ perfil:'anon|admin|aluno|prof', w:1440, h:900, path:'/', out:'nome.png', full:true, eval:'() => ...' }]
import { createRequire } from 'module';
import fs from 'fs';

const require = createRequire('/home/edivaldo/.npm/_npx/e41f203b7505f1fb/node_modules/x.js');
const { chromium } = require('playwright');

const BASE = 'http://localhost:4002';
const SAIDA = (process.env.SAIDA || '/tmp/redesign-shots') + '/';
const CREDS = { admin: ['admin', 'admin-visual-123'], aluno: ['aluno1', 'senha123'], prof: ['prof', 'prof12345'] };
fs.mkdirSync(SAIDA, { recursive: true });

const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const browser = await chromium.launch({
  executablePath: '/home/edivaldo/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome',
  args: ['--no-sandbox'],
});
const contextos = {};

async function contexto(perfil, w, h) {
  const chave = `${perfil}|${w}x${h}`;
  if (contextos[chave]) return contextos[chave];
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, reducedMotion: 'reduce' });
  if (perfil !== 'anon') {
    const p = await ctx.newPage();
    await p.goto(BASE + '/login', { waitUntil: 'networkidle' });
    const form = p.locator('form[action="/login"]').first();
    await form.locator('input:not([type=hidden]):not([type=checkbox]):not([type=password])').first().fill(CREDS[perfil][0]);
    await form.locator('input[type=password]').first().fill(CREDS[perfil][1]);
    await Promise.all([p.waitForNavigation({ waitUntil: 'networkidle' }), form.locator('[type=submit]').first().click()]);
    console.log(`login ${perfil} ${w}x${h} -> ${p.url()}`);
    await p.close();
  }
  return (contextos[chave] = ctx);
}

for (const j of jobs) {
  const ctx = await contexto(j.perfil || 'anon', j.w || 1440, j.h || 900);
  const page = await ctx.newPage();
  const erros = [];
  page.on('console', (m) => { if (m.type() === 'error') erros.push(m.text().slice(0, 160)); });
  page.on('pageerror', (e) => erros.push('pageerror: ' + String(e).slice(0, 160)));
  const resp = await page.goto(BASE + j.path, { waitUntil: 'networkidle' });
  for (const sel of j.cliques || []) { await page.locator(sel).first().click(); await page.waitForTimeout(400); }
  const resumo = {
    out: j.out, url: page.url().replace(BASE, ''), status: resp && resp.status(),
    overflowX: await page.evaluate(() => document.documentElement.scrollWidth - innerWidth),
    erros,
  };
  if (j.eval) resumo.eval = await page.evaluate(`(${j.eval})()`);
  if (j.out) await page.screenshot({ path: SAIDA + j.out, fullPage: j.full !== false });
  console.log(JSON.stringify(resumo));
  await page.close();
}
await browser.close();
