// Varredura de QA do redesign: audita cada tela e cada modal (desktop 1440 e celular 390), roda
// fluxos funcionais e confere o controle de acesso entre perfis.
// Uso: SAIDA=/tmp/redesign-varredura node tools/redesign/varredura.mjs   (instância em :4002)
// Só lê e abre/fecha modais. Nunca confirma uma ação destrutiva.
import { createRequire } from 'module';
import fs from 'fs';
import zlib from 'zlib';

const require = createRequire('/home/edivaldo/.npm/_npx/e41f203b7505f1fb/node_modules/x.js');
const { chromium } = require('playwright');

const BASE = process.env.BASE || 'http://localhost:4002';
const SAIDA = (process.env.SAIDA || '/tmp/redesign-varredura') + '/';
fs.mkdirSync(SAIDA, { recursive: true });

const CREDS = {
  admin: ['admin', 'admin-visual-123'], aluno: ['aluno1', 'senha123'],
  aluno_vazio: ['aluno9', 'senha123'], prof: ['prof', 'prof12345'],
};
const VIEWPORTS = [{ n: 'd', w: 1440, h: 900 }, { n: 'm', w: 390, h: 844 }];

// ----------------------------------------------------------------------------- páginas
const P = (perfil, path, nome, extra = {}) => ({ perfil, path, nome, ...extra });
const CONF = { confirmacoes: true };
const PAGINAS = [
  P('anon', '/', 'home', { modais: [{ id: 'login', abrir: '[data-abrir-login]', dialogo: '#meuModal', backdrop: '[data-fechar-login]' }] }),
  P('anon', '/login', 'login'), P('anon', '/cadastrar', 'cadastro'), P('anon', '/recuperar_senha', 'recuperar'),
  P('anon', '/recuperar_senha/token-invalido', 'redefinir-invalido'), P('anon', '/ativar-acesso/token-invalido', 'ativar-invalido'),
  P('anon', '/termos-de-responsabilidade', 'termos'),
  ...['visao-geral', 'turmas', 'mensalidades', 'planos', 'meus-dados'].map((a) =>
    P('aluno', `/perfil#${a}`, `aluno-${a}`, {
      ...CONF, mockPix: true,
      modais: a === 'visao-geral' ? [{ id: 'pix', abrir: '[data-pix-pagar]', dialogo: '#pix-dialog', fechar: '[data-pix-fechar]' }]
        : a === 'turmas' ? [
          { id: 'turma', abrir: '[data-abrir-turma]', dialogo: '#turma-dialog', fechar: '[data-turma-fechar]' },
          { id: 'presencas', abrir: '[data-abrir-presencas]', dialogo: '#presenca-dialog', fechar: '[data-presenca-fechar]' }] : [],
    })),
  P('aluno', '/perfil/pagamento/2', 'aluno-pagamento', { mockPix: true }),
  P('aluno', '/perfil/mensalidade/2/comprovante', 'aluno-comprovante'),
  ...['visao-geral', 'turmas', 'mensalidades', 'planos', 'meus-dados'].map((a) => P('aluno_vazio', `/perfil#${a}`, `vazio-${a}`, { ...CONF })),
  P('prof', '/professor', 'prof-home', CONF), P('prof', '/turmas/1', 'prof-turma', CONF),
  P('admin', '/admin', 'admin-painel', CONF), P('admin', '/admin/turmas', 'admin-turmas', CONF),
  P('admin', '/turmas/1', 'admin-turma', CONF),
  P('admin', '/admin/financeiro', 'admin-financeiro', { ...CONF, modais: [{ id: 'comprovante', abrir: '[data-abrir-comprovante]', dialogo: '#comprovante-dialog', fechar: '[data-comprovante-fechar]' }] }),
  P('admin', '/admin/avisos', 'admin-avisos', CONF), P('admin', '/admin/academia', 'admin-academia', CONF),
  P('admin', '/admin/alunos/novo', 'admin-aluno-novo', CONF),
  P('admin', '/admin/usuario/00000000001', 'admin-perfil-aluno', { ...CONF, mockPix: true }),
  P('admin', '/admin/usuario/00000000008', 'admin-perfil-longo', CONF),
  P('admin', '/admin/professores/1/editar', 'admin-prof-editar', CONF),
];

// ----------------------------------------------------------------------------- auditoria no navegador
function auditar(seletorRaiz) {
  const raiz = seletorRaiz ? document.querySelector(seletorRaiz) : document.body;
  const out = { overflowX: document.documentElement.scrollWidth - innerWidth };
  const visivel = (e) => {
    const r = e.getBoundingClientRect(); const cs = getComputedStyle(e);
    return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' && parseFloat(cs.opacity) > 0.05;
  };
  const nome = (e) => (e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') +
    (typeof e.className === 'string' && e.className.trim() ? '.' + e.className.trim().split(/\s+/).slice(0, 2).join('.') : '')).slice(0, 64);
  const todos = [...raiz.querySelectorAll('*')].filter(visivel);

  // contraste (WCAG) calculado com o fundo efetivo; pula elementos sobre gradiente/imagem
  const rgba = (c) => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return [0, 0, 0, 0]; const p = m[1].split(/[\s,\/]+/).filter(Boolean).map(Number); return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1]; };
  const lum = (r, g, b) => { const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
  const fundo = (el) => {
    const camadas = [];
    for (let e = el; e; e = e.parentElement) {
      const cs = getComputedStyle(e); if (cs.backgroundImage !== 'none') return null;
      const b = rgba(cs.backgroundColor); camadas.push(b); if (b[3] >= 1) break;
    }
    let base = rgba(getComputedStyle(document.documentElement).backgroundColor); if (base[3] === 0) base = [255, 255, 255, 1];
    let [r, g, b] = base;
    for (let i = camadas.length - 1; i >= 0; i--) { const [cr, cg, cb, ca] = camadas[i]; r = cr * ca + r * (1 - ca); g = cg * ca + g * (1 - ca); b = cb * ca + b * (1 - ca); }
    return [r, g, b];
  };
  const falhas = []; const vistos = new Set();
  for (const el of todos) {
    if (![...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())) continue;
    const cs = getComputedStyle(el); const f = fundo(el); if (!f) continue;
    const c = rgba(cs.color); const a = c[3];
    const fg = [c[0] * a + f[0] * (1 - a), c[1] * a + f[1] * (1 - a), c[2] * a + f[2] * (1 - a)];
    const L1 = lum(...fg), L2 = lum(...f); const razao = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
    const px = parseFloat(cs.fontSize); const neg = parseInt(cs.fontWeight) >= 700;
    const min = (px >= 24 || (px >= 18.66 && neg)) ? 3 : 4.5;
    if (razao < min) {
      const txt = el.textContent.trim().replace(/\s+/g, ' ').slice(0, 38); const k = txt + razao.toFixed(1);
      if (!vistos.has(k)) { vistos.add(k); falhas.push(`${nome(el)} "${txt}" ${razao.toFixed(2)}<${min} (${cs.color} sobre rgb(${f.map(Math.round)}))`); }
    }
  }
  out.contraste = falhas.slice(0, 10); out.contrasteTotal = falhas.length;

  const emRolagem = (e) => { for (let p = e.parentElement; p && p !== document.body; p = p.parentElement) { if (/(auto|scroll|hidden|clip)/.test(getComputedStyle(p).overflowX)) return true; } return false; };
  out.foraDaTela = todos.filter((e) => { const r = e.getBoundingClientRect(); return (r.right > innerWidth + 1 || r.left < -1) && getComputedStyle(e).position !== 'fixed' && !emRolagem(e); })
    .slice(0, 6).map((e) => { const r = e.getBoundingClientRect(); return `${nome(e)} ${Math.round(r.left)}..${Math.round(r.right)}`; });
  out.cortado = todos.filter((e) => { const cs = getComputedStyle(e); return /(hidden|clip)/.test(cs.overflowX) && e.clientWidth > 2 && e.scrollWidth > e.clientWidth + 2 && cs.textOverflow !== 'ellipsis' && [...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim()); })
    .slice(0, 6).map((e) => `${nome(e)} ${e.scrollWidth}>${e.clientWidth}`);

  const imgs = [...raiz.querySelectorAll('img')].filter(visivel);
  out.imgQuebrada = imgs.filter((i) => i.complete && i.naturalWidth === 0).map((i) => i.src.split('/').slice(-2).join('/'));
  out.imgAmpliada = imgs.filter((i) => i.naturalWidth > 0 && !/\.svg/.test(i.src) && !/^data:/.test(i.src) && i.getBoundingClientRect().width / i.naturalWidth > 1.15)
    .map((i) => `${i.src.split('/').pop()} ${i.naturalWidth}->${Math.round(i.getBoundingClientRect().width)}`);
  out.imgSemAlt = imgs.filter((i) => !i.hasAttribute('alt')).length;

  out.semNome = [...raiz.querySelectorAll('a[href],button,[role=button],input:not([type=hidden]),select,textarea')].filter(visivel).filter((e) => {
    const al = e.getAttribute('aria-label') || e.getAttribute('title') || e.getAttribute('aria-labelledby');
    if (/^(INPUT|SELECT|TEXTAREA)$/.test(e.tagName)) return !(al || (e.labels && e.labels.length));
    return !((e.innerText || '').trim() || al || e.querySelector('img[alt]:not([alt=""])'));
  }).slice(0, 6).map(nome);

  const ids = {}; document.querySelectorAll('[id]').forEach((e) => { ids[e.id] = (ids[e.id] || 0) + 1; });
  out.idsDup = Object.entries(ids).filter(([, n]) => n > 1).map(([k, n]) => `${k}x${n}`);

  if (innerWidth <= 430) {
    out.alvoPequeno = [...raiz.querySelectorAll('a[href],button,select,input[type=checkbox],input[type=radio]')].filter(visivel).filter((e) => {
      if (getComputedStyle(e).display === 'inline') return false; const r = e.getBoundingClientRect(); return Math.min(r.width, r.height) < 32;
    }).slice(0, 8).map((e) => { const r = e.getBoundingClientRect(); return `${nome(e)} ${Math.round(r.width)}x${Math.round(r.height)}`; });
  }
  const t = raiz.innerText || '';
  out.vazamentos = [...new Set((t.match(/\b(undefined|null|NaN|None)\b|\{\{|\{%|Traceback|Internal Server Error/g)) || [])];
  out.fonte = document.fonts.check('20px "Bebas Neue"');
  return out;
}

// ----------------------------------------------------------------------------- utilidades
const problemas = []; const notas = [];
const reg = (onde, tipo, detalhe) => problemas.push({ onde, tipo, detalhe });

function resumoAuditoria(onde, a) {
  if (!a) return;
  if (a.overflowX > 0) reg(onde, 'rolagem horizontal', `${a.overflowX}px`);
  if (a.contrasteTotal) reg(onde, `contraste baixo (${a.contrasteTotal})`, a.contraste.join(' | '));
  if (a.foraDaTela.length) reg(onde, 'fora da tela', a.foraDaTela.join(' | '));
  if (a.cortado.length) reg(onde, 'texto cortado', a.cortado.join(' | '));
  if (a.imgQuebrada.length) reg(onde, 'imagem quebrada', a.imgQuebrada.join(' | '));
  if (a.imgAmpliada.length) reg(onde, 'imagem ampliada (borrada)', a.imgAmpliada.join(' | '));
  if (a.semNome.length) reg(onde, 'controle sem nome acessível', a.semNome.join(' | '));
  if (a.idsDup.length) reg(onde, 'ids duplicados', a.idsDup.join(' | '));
  if (a.alvoPequeno && a.alvoPequeno.length) reg(onde, 'alvo de toque < 32px', a.alvoPequeno.join(' | '));
  if (a.vazamentos.length) reg(onde, 'texto vazado (template/None/undefined)', a.vazamentos.join(', '));
  if (a.imgSemAlt) reg(onde, 'img sem atributo alt', String(a.imgSemAlt));
  if (a.fonte === false) reg(onde, 'fonte Bebas Neue não carregou', '');
}

const crc = (() => { const t = []; for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } return (b) => { let c = 0xffffffff; for (const x of b) c = t[(c ^ x) & 255] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0; }; })();
function pngQr() { // "QR" falso 25x25 módulos, 8px cada: só para testar layout
  const N = 25, S = 8, W = N * S; const raw = Buffer.alloc((W * 3 + 1) * W);
  for (let y = 0; y < W; y++) { raw[y * (W * 3 + 1)] = 0; for (let x = 0; x < W; x++) { const m = ((Math.floor(x / S) * 7 + Math.floor(y / S) * 13) % 5) < 2; const o = y * (W * 3 + 1) + 1 + x * 3; raw[o] = raw[o + 1] = raw[o + 2] = m ? 0 : 255; } }
  const ch = (tipo, d) => { const l = Buffer.alloc(4); l.writeUInt32BE(d.length); const td = Buffer.concat([Buffer.from(tipo), d]); const c = Buffer.alloc(4); c.writeUInt32BE(crc(td)); return Buffer.concat([l, td, c]); };
  const ihdr = Buffer.alloc(13); ihdr.writeUInt32BE(W, 0); ihdr.writeUInt32BE(W, 4); ihdr[8] = 8; ihdr[9] = 2;
  return Buffer.concat([Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]), ch('IHDR', ihdr), ch('IDAT', zlib.deflateSync(raw)), ch('IEND', Buffer.alloc(0))]).toString('base64');
}
const QR = pngQr();
const PIX_OK = { status: 'pendente', status_rotulo: 'Pendente', valor: 150, vencimento: '2026-09-28', pix_copia_cola: '00020126580014BR.GOV.BCB.PIX0136a1b2c3d4-e5f6-7890-abcd-ef1234567890520400005303986540515.005802BR5913EXTREME TEAM6009FORTALEZA62070503***6304ABCD', qr_code_base64: QR, pix_expirado: false };

async function preparar(page, job) {
  if (job.mockPix) {
    await page.route('**/api/mensalidades/*/pix', (r) => r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(PIX_OK) }));
    await page.route('**/api/mensalidades/*/status', (r) => r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(PIX_OK) }));
  }
}
const aberto = (page, sel) => page.evaluate((s) => { const d = document.querySelector(s); if (!d) return false; return d.tagName === 'DIALOG' ? d.open : (!d.hidden && getComputedStyle(d).display !== 'none'); }, sel);

async function testaModal(page, m, v, base) {
  const onde = `${base} [${v.n}] modal ${m.id}`; const gatilho = page.locator(m.abrir).first();
  if (!(await gatilho.count()) || !(await gatilho.isVisible().catch(() => false))) { notas.push(`${onde}: gatilho não visível (sem dado para abrir)`); return; }
  const antes = page.url();
  await gatilho.scrollIntoViewIfNeeded().catch(() => {});
  await gatilho.click({ timeout: 4000 }).catch((e) => reg(onde, 'gatilho não clicável', e.message.split('\n')[0]));
  await page.waitForTimeout(700);
  if (!(await aberto(page, m.dialogo))) { reg(onde, 'modal não abriu', `url mudou: ${page.url() !== antes}`); if (page.url() !== antes) await page.goto(antes); return; }
  const info = await page.evaluate((s) => {
    const d = document.querySelector(s); const c = d.querySelector('.modal-conteudo, .modal-dialog-corpo, form, div') || d; const b = (d.tagName === 'DIALOG' ? d : c).getBoundingClientRect();
    return { foco: d.contains(document.activeElement), dentroDaTela: b.left >= -1 && b.right <= innerWidth + 1 && b.top >= -1 && b.bottom <= innerHeight + 1, alt: Math.round(b.height), vh: innerHeight, larg: Math.round(b.width), vw: innerWidth, rolaInterno: d.scrollHeight > d.clientHeight + 2 };
  }, m.dialogo);
  if (!info.foco) reg(onde, 'foco não entrou no modal', '');
  if (!info.dentroDaTela && !info.rolaInterno) reg(onde, 'modal maior que a tela sem rolagem', `${info.larg}x${info.alt} em ${info.vw}x${info.vh}`);
  resumoAuditoria(onde, await page.evaluate(auditar, m.dialogo));
  await page.screenshot({ path: `${SAIDA}${base}-modal-${m.id}-${v.n}.png` });
  await page.keyboard.press('Escape'); await page.waitForTimeout(350);
  if (await aberto(page, m.dialogo)) {
    reg(onde, 'Esc não fecha o modal', '');
    const alvo = m.fechar || m.backdrop; if (alvo) await page.locator(alvo).first().click({ timeout: 2000 }).catch(() => {});
    await page.waitForTimeout(300);
  }
  if (m.backdrop) { // reabre e fecha clicando fora
    await gatilho.click({ timeout: 3000 }).catch(() => {}); await page.waitForTimeout(400);
    await page.locator(m.backdrop).first().click({ position: { x: 4, y: 4 }, force: true, timeout: 2000 }).catch(() => {}); await page.waitForTimeout(350);
    if (await aberto(page, m.dialogo)) { reg(onde, 'clique fora não fecha o modal', ''); await page.keyboard.press('Escape'); }
  }
}

async function confirmacoes(page, v, base) {
  const gat = page.locator('form[data-confirm-modal] [type=submit]'); const n = await gat.count(); let primeiro = true;
  for (let i = 0; i < n; i++) {
    const g = gat.nth(i); if (!(await g.isVisible().catch(() => false))) continue;
    const rot = ((await g.innerText().catch(() => '')) || (await g.getAttribute('aria-label')) || `#${i}`).trim().replace(/\s+/g, ' ').slice(0, 28);
    const onde = `${base} [${v.n}] confirmar "${rot}"`; const antes = page.url();
    await g.scrollIntoViewIfNeeded().catch(() => {}); await g.click({ timeout: 3000 }).catch(() => {}); await page.waitForTimeout(450);
    if (!(await aberto(page, '#confirm-dialog'))) { reg(onde, 'diálogo de confirmação não abriu', `url mudou: ${page.url() !== antes} (a ação pode ter sido enviada sem confirmar!)`); if (page.url() !== antes) await page.goto(antes); continue; }
    const txt = await page.evaluate(() => ({ t: (document.getElementById('confirm-dialog-title') || {}).textContent, m: (document.getElementById('confirm-dialog-message') || {}).textContent, b: [...document.querySelectorAll('#confirm-dialog button')].map((x) => x.textContent.trim()) }));
    if (!txt.t || !txt.t.trim()) reg(onde, 'confirmação sem título', JSON.stringify(txt));
    if (!txt.m || !txt.m.trim()) reg(onde, 'confirmação sem mensagem', JSON.stringify(txt));
    if (!txt.b.some(Boolean)) reg(onde, 'confirmação sem rótulo nos botões', JSON.stringify(txt.b));
    resumoAuditoria(onde, await page.evaluate(auditar, '#confirm-dialog'));
    if (primeiro) { await page.screenshot({ path: `${SAIDA}${base}-modal-confirmar-${v.n}.png` }); primeiro = false; }
    await page.keyboard.press('Escape'); await page.waitForTimeout(300);
    if (await aberto(page, '#confirm-dialog')) reg(onde, 'Esc não fecha a confirmação', '');
    if (page.url() !== antes) { reg(onde, 'a página navegou ao cancelar', page.url()); await page.goto(antes); }
  }
}

// ----------------------------------------------------------------------------- execução
const browser = await chromium.launch({ executablePath: '/home/edivaldo/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome', args: ['--no-sandbox'] });
const ctxs = {};
async function ctx(perfil, v) {
  const k = `${perfil}|${v.n}`; if (ctxs[k]) return ctxs[k];
  const c = await browser.newContext({ viewport: { width: v.w, height: v.h }, reducedMotion: 'reduce' });
  if (perfil !== 'anon') {
    const p = await c.newPage(); await p.goto(BASE + '/login', { waitUntil: 'networkidle' });
    const f = p.locator('form[action="/login"]').first();
    await f.locator('input:not([type=hidden]):not([type=checkbox]):not([type=password])').first().fill(CREDS[perfil][0]);
    await f.locator('input[type=password]').first().fill(CREDS[perfil][1]);
    await Promise.all([p.waitForNavigation({ waitUntil: 'networkidle' }), f.locator('[type=submit]').first().click()]);
    notas.push(`login ${perfil} [${v.n}] -> ${p.url().replace(BASE, '')}`); await p.close();
  }
  return (ctxs[k] = c);
}

for (const job of PAGINAS) {
  for (const v of VIEWPORTS) {
    const onde = `${job.nome} [${v.n}]`;
    try {
      const page = await (await ctx(job.perfil, v)).newPage();
      const erros = []; const rede = [];
      page.on('console', (m) => { if (m.type() === 'error') erros.push(m.text().slice(0, 140)); });
      page.on('pageerror', (e) => erros.push('pageerror: ' + String(e).slice(0, 140)));
      page.on('response', (r) => { if (r.status() >= 400 && !/\/api\/mensalidades\//.test(r.url())) rede.push(`${r.status()} ${r.url().replace(BASE, '')}`); });
      page.on('requestfailed', (r) => { if (!/fonts\.g/.test(r.url())) rede.push(`FALHA ${r.url().replace(BASE, '').slice(0, 80)}`); });
      await preparar(page, job);
      const resp = await page.goto(BASE + job.path, { waitUntil: 'networkidle' });
      await page.waitForTimeout(500);
      const st = resp && resp.status();
      const esperado404 = /invalido/.test(job.nome) ? [200, 302, 400, 404] : [200];
      if (!esperado404.includes(st)) reg(onde, `status HTTP ${st}`, job.path);
      if (new URL(page.url()).pathname !== new URL(BASE + job.path).pathname) reg(onde, 'redirecionou', `${job.path} -> ${page.url().replace(BASE, '')}`);
      const a = await page.evaluate(auditar, null);
      resumoAuditoria(onde, a);
      if (erros.length) reg(onde, 'erro de console', [...new Set(erros)].join(' | '));
      if (rede.length) reg(onde, 'requisição com erro', [...new Set(rede)].join(' | '));
      await page.screenshot({ path: `${SAIDA}${job.nome}-${v.n}.png`, fullPage: true });
      for (const m of job.modais || []) await testaModal(page, m, v, job.nome);
      if (job.confirmacoes) await confirmacoes(page, v, job.nome);
      await page.close();
    } catch (e) { reg(onde, 'EXCEÇÃO na varredura', e.message.split('\n')[0]); }
  }
}

// ----------------------------------------------------------------------------- controle de acesso
const ACESSO = [
  ['anon', '/admin'], ['anon', '/admin/financeiro'], ['anon', '/perfil'], ['anon', '/professor'], ['anon', '/turmas/1'],
  ['aluno', '/admin'], ['aluno', '/admin/financeiro'], ['aluno', '/professor'], ['aluno', '/admin/usuario/00000000001'],
  ['prof', '/admin'], ['prof', '/admin/financeiro'], ['prof', '/perfil'],
  ['admin', '/perfil'], ['admin', '/professor'],
];
for (const [perfil, path] of ACESSO) {
  const p = await (await ctx(perfil, VIEWPORTS[0])).newPage();
  const r = await p.goto(BASE + path, { waitUntil: 'networkidle' });
  const fim = new URL(p.url()).pathname; const corpo = (await p.locator('body').innerText().catch(() => '')).slice(0, 60).replace(/\s+/g, ' ');
  if (!(fim === '/login' || r.status() === 403 || r.status() === 401)) reg(`acesso ${perfil} -> ${path}`, 'perfil sem permissão NÃO foi barrado', `${r.status()} ${fim} "${corpo}"`);
  else notas.push(`acesso ${perfil} -> ${path}: barrado (${fim}, ${r.status()})`);
  await p.close();
}

// ----------------------------------------------------------------------------- fluxos funcionais
async function fluxo(nome, fn, perfil = 'anon', v = VIEWPORTS[0]) {
  const page = await (await ctx(perfil, v)).newPage();
  try { const r = await fn(page); if (r) reg(`fluxo: ${nome} [${v.n}]`, 'falhou', r); else notas.push(`fluxo OK: ${nome} [${v.n}]`); }
  catch (e) { reg(`fluxo: ${nome} [${v.n}]`, 'EXCEÇÃO', e.message.split('\n')[0]); }
  await page.close();
}
const ir = (p, u) => p.goto(BASE + u, { waitUntil: 'networkidle' });
await fluxo('login com senha errada mostra erro', async (p) => {
  await ir(p, '/login'); await p.fill('#loginusuario', 'aluno1'); await p.fill('#senhausuario', 'errada-123');
  await Promise.all([p.waitForNavigation({ waitUntil: 'networkidle' }), p.click('.auth-submit-btn')]);
  const t = await p.locator('.alert').first().innerText().catch(() => ''); if (!t.trim()) return 'nenhuma mensagem de erro visível'; if (!p.url().includes('/login')) return `foi para ${p.url()}`;
});
await fluxo('mostrar/ocultar senha alterna o tipo', async (p) => {
  await ir(p, '/login'); const t0 = await p.getAttribute('#senhausuario', 'type'); await p.click('.password-toggle'); const t1 = await p.getAttribute('#senhausuario', 'type'); await p.click('.password-toggle'); const t2 = await p.getAttribute('#senhausuario', 'type');
  if (!(t0 === 'password' && t1 === 'text' && t2 === 'password')) return `tipos: ${t0} -> ${t1} -> ${t2}`;
});
await fluxo('⇄ leva do login ao cadastro e volta', async (p) => {
  await ir(p, '/login'); await Promise.all([p.waitForURL('**/cadastrar', { timeout: 4000 }), p.click('.flow-swap-btn')]);
  await p.waitForLoadState('networkidle'); await Promise.all([p.waitForURL('**/login', { timeout: 4000 }), p.click('.flow-swap-btn')]);
});
await fluxo('abas do celular alternam login/cadastro', async (p) => {
  await ir(p, '/login'); await Promise.all([p.waitForURL('**/cadastrar', { timeout: 4000 }), p.click('.auth-tab:not(.active)')]);
  const ativa = await p.locator('.auth-tab[aria-current="page"]').innerText(); if (!/criar/i.test(ativa)) return `aba ativa: ${ativa}`;
}, 'anon', VIEWPORTS[1]);
await fluxo('"lembrar meu usuário" guarda e preenche o usuário (nunca a senha)', async (p) => {
  await ir(p, '/login'); await p.fill('#loginusuario', 'aluno1'); await p.fill('#senhausuario', 'errada-123'); await p.check('#lembrar_usuario');
  await Promise.all([p.waitForNavigation({ waitUntil: 'networkidle' }), p.click('.auth-submit-btn')]);
  const salvo = await p.evaluate(() => JSON.stringify(Object.entries(localStorage))); if (/errada-123/.test(salvo)) return 'a SENHA foi gravada no localStorage';
  const v1 = await p.inputValue('#loginusuario'); if (v1 !== 'aluno1') return `usuário não preenchido após recarregar: "${v1}"`;
});
await fluxo('modal de login da landing entra como aluno', async (p) => {
  await ir(p, '/'); await p.click('.nav-login'); await p.waitForTimeout(400);
  await p.fill('#inputnome', 'aluno1'); await p.fill('#senhausuario', 'senha123');
  await Promise.all([p.waitForNavigation({ waitUntil: 'networkidle' }), p.click('#meuModal button[type=submit]')]);
  if (!p.url().includes('/perfil')) return `foi para ${p.url()}`;
});
await fluxo('botão "ver" da senha no modal da landing alterna', async (p) => {
  await ir(p, '/'); await p.click('.nav-login'); await p.waitForTimeout(400); const t0 = await p.getAttribute('#meuModal #senhausuario', 'type');
  await p.click('#iconeSenha'); const t1 = await p.getAttribute('#meuModal #senhausuario', 'type'); if (!(t0 === 'password' && t1 === 'text')) return `${t0} -> ${t1}`;
});
await fluxo('cadastro: senhas diferentes mostram o aviso e bloqueiam o envio', async (p) => {
  await ir(p, '/cadastrar'); await p.fill('#senhausuario', 'Forte#Senha-2026'); await p.fill('#confirmarsenhausuario', 'outra-coisa-999'); await p.locator('#confirmarsenhausuario').blur();
  await p.waitForTimeout(300); const vis = await p.locator('#confirmarsenhausuario-erro').isVisible(); if (!vis) return 'aviso de senhas diferentes não apareceu';
});
await fluxo('cadastro: envio vazio é barrado pelo navegador', async (p) => {
  await ir(p, '/cadastrar'); await p.click('.auth-submit-btn'); await p.waitForTimeout(400); if (new URL(p.url()).pathname !== '/cadastrar') return `saiu para ${p.url()}`;
  const inv = await p.evaluate(() => document.querySelectorAll('#cadastro-form :invalid').length); if (!inv) return 'nenhum campo inválido detectado';
});
await fluxo('recuperar senha com dados inexistentes responde sem erro 500', async (p) => {
  await ir(p, '/recuperar_senha'); await p.fill('#cpf', '000.000.000-00'); await p.fill('input[type=email]', 'nao@existe.com');
  const [r] = await Promise.all([p.waitForNavigation({ waitUntil: 'networkidle' }), p.click('#recuperar-form [type=submit]')]);
  if (r && r.status() >= 500) return `HTTP ${r.status()}`; const t = (await p.locator('body').innerText()).trim(); if (t.length < 20) return 'página vazia';
});
await fluxo('sair do painel (confirma no diálogo) encerra a sessão', async (p) => {
  await ir(p, '/admin'); await p.click('.admin-header .logout-form [type=submit]'); await p.waitForTimeout(400);
  if (!(await aberto(p, '#confirm-dialog'))) return 'diálogo não abriu';
  await Promise.all([p.waitForNavigation({ waitUntil: 'networkidle' }), p.click('#confirm-dialog [data-modal-accept]')]);
  const r = await p.goto(BASE + '/admin', { waitUntil: 'networkidle' }); if (!new URL(p.url()).pathname.includes('login')) return `ainda logado: ${p.url()} (${r.status()})`;
}, 'admin');

await browser.close();

// ----------------------------------------------------------------------------- relatório
fs.writeFileSync(SAIDA + 'relatorio.json', JSON.stringify({ problemas, notas }, null, 2));
const porTipo = {}; for (const p of problemas) (porTipo[p.tipo.replace(/\s*\(\d+\)/, '')] ||= []).push(p);
console.log(`\n=== ${problemas.length} ocorrências em ${new Set(problemas.map((p) => p.onde)).size} lugares ===`);
for (const [tipo, lista] of Object.entries(porTipo).sort((a, b) => b[1].length - a[1].length)) {
  console.log(`\n## ${tipo}  (${lista.length})`);
  for (const p of lista.slice(0, 40)) console.log(`- ${p.onde}: ${String(p.detalhe).slice(0, 260)}`);
}
console.log(`\n(${notas.length} verificações OK/notas em relatorio.json; capturas em ${SAIDA})`);
