// Fase 3b da biblioteca no Figma (ver LEIA-ME.md). Rodar pelo use_figma com
// fileKey zam95scFOGbSjkrdukfpse. Idempotente: recria cada seção pelo nome.
// Campo + Grupo de campo, Caixa, Interruptor + Linha do interruptor, Aviso, e rótulos
// de linha/coluna nas grades de Botão e Selo (já criados na Fase 3a).
const page = await figma.getNodeByIdAsync('4:5');
await figma.setCurrentPageAsync(page);
const vars = await figma.variables.getLocalVariablesAsync();
const cols = await figma.variables.getLocalVariableCollectionsAsync();
const col = n => cols.find(c => c.name === n);
const V = (n, c = 'Cor') => { const v = vars.find(v => v.name === n && v.variableCollectionId === col(c).id); if (!v) throw new Error('variável ' + c + ':' + n); return v; };
const VE = n => { try { return V(n, 'Cor no escuro'); } catch (e) { return V(n); } };
const D = n => V(n, 'Dimensões');
const pintar = (v, opacity = 1) => [figma.variables.setBoundVariableForPaint({ type: 'SOLID', color: { r: 0, g: 0, b: 0 }, opacity }, 'color', v)];
const bind = (n, campos, v) => campos.forEach(c => n.setBoundVariable(c, v));
const PAD = ['paddingTop', 'paddingBottom', 'paddingLeft', 'paddingRight'];
const RAIO = ['topLeftRadius', 'topRightRadius', 'bottomLeftRadius', 'bottomRightRadius'];
await figma.loadFontAsync({ family: 'Bebas Neue', style: 'Regular' });
for (const s of ['Regular', 'Medium', 'Semi Bold', 'Bold']) await figma.loadFontAsync({ family: 'Inter', style: s });
const ts = await figma.getLocalTextStylesAsync();
const T = n => { const s = ts.find(s => s.name === n); if (!s) throw new Error('estilo ' + n); return s; };
async function texto(pai, conteudo, estilo, corVar) {
  const t = figma.createText(); await t.setTextStyleIdAsync(T(estilo).id);
  t.characters = conteudo; t.fills = pintar(corVar); if (pai) pai.appendChild(t); return t;
}
const sh = (spread, r, g, b, a) => ({ type: 'DROP_SHADOW', color: { r, g, b, a }, offset: { x: 0, y: 0 }, radius: 0, spread, visible: true, blendMode: 'NORMAL', showShadowBehindNode: false });
function fundoSecao() {
  const outras = page.children.filter(n => n.type === 'SECTION');
  return outras.length ? Math.max(...outras.map(n => n.y + n.height)) + 160 : 0;
}
async function novaSecao(nome, descricao) {
  page.children.filter(n => n.name === nome && n.type === 'SECTION').forEach(n => n.remove());
  const s = figma.createSection(); s.name = nome; s.x = 0; s.y = fundoSecao();
  s.fills = pintar(V('cor/fundo/pagina'));
  const doc = figma.createAutoLayout('VERTICAL', { name: 'Documentação' }); s.appendChild(doc);
  doc.x = 64; doc.y = 64; doc.fills = []; bind(doc, ['itemSpacing'], D('espaco/3'));
  await texto(doc, nome, 'Display/H1', V('cor/texto/padrao'));
  const d = await texto(doc, descricao, 'Corpo/SM', V('cor/texto/secundario')); d.textAutoResize = 'HEIGHT'; d.resize(720, d.height);
  return s;
}
function encaixar(secao) {
  let w = 0, h = 0;
  for (const f of secao.children) { w = Math.max(w, f.x + f.width); h = Math.max(h, f.y + f.height); }
  secao.resizeWithoutConstraints(Math.max(w + 64, 960), h + 64);
}
function moldura(set) {
  set.fills = pintar(V('cor/fundo/superficie')); set.strokes = pintar(V('cor/borda/padrao')); set.strokeWeight = 1; set.dashPattern = [6, 4];
  bind(set, RAIO, D('raio/cartao'));
}
function grade(set, linhas, colunas, chave, gap = 24, pad = 32) {
  const larg = {}, alt = {};
  for (const c of set.children) { const [l, k] = chave(c); larg[k] = Math.max(larg[k] || 0, c.width); alt[l] = Math.max(alt[l] || 0, c.height); }
  const xs = {}, ys = {}; let x = pad; for (const k of colunas) { xs[k] = x; x += larg[k] + gap; }
  let y = pad; for (const l of linhas) { ys[l] = y; y += alt[l] + gap; }
  for (const c of set.children) { const [l, k] = chave(c); c.x = xs[k]; c.y = ys[l] + (alt[l] - c.height) / 2; }
  set.resizeWithoutConstraints(x - gap + pad, y - gap + pad); moldura(set);
  return { xs, ys, larg, alt };
}
// rótulos de linha/coluna fora do conjunto (na seção), para ler a grade
async function rotular(secao, set, g, linhas, colunas) {
  const grupo = [];
  for (const l of linhas) { const t = await texto(secao, l, 'Micro/Caixa alta', V('cor/texto/secundario')); t.x = set.x - t.width - 20; t.y = set.y + g.ys[l] + g.alt[l] / 2 - t.height / 2; grupo.push(t); }
  for (const k of colunas) { const t = await texto(secao, k, 'Micro/Caixa alta', V('cor/texto/secundario')); t.x = set.x + g.xs[k]; t.y = set.y - t.height - 12; grupo.push(t); }
  if (grupo.length) { const gr = figma.group(grupo, secao); gr.name = 'Rótulos da grade · ' + set.name; }
}
const prop = (c, n) => c.variantProperties[n];
const icone = n => page.findOne(x => x.type === 'COMPONENT' && x.name === `Ícone/${n}`);
function pintarIcone(inst, corVar) {
  for (const n of inst.findAll(n => 'strokes' in n)) { if (n.strokes && n.strokes.length) n.strokes = pintar(corVar); if (n.type === 'ELLIPSE') n.fills = pintar(corVar); }
}

// ---- rótulos para Botão e Selo (já criados)
for (const [nomeSecao, linhas, colunas, chave, gap] of [
  ['Botão', ['Principal', 'Secundário', 'Contorno', 'Fantasma', 'Link', 'Confirmar', 'Perigo', 'Destrutivo'], ['Pequeno', 'Padrão', 'Grande'], c => [prop(c, 'Variante'), prop(c, 'Tamanho')], 24],
  ['Selo', ['Simples', 'Situação'], ['Padrão', 'Ok', 'Alerta', 'Perigo', 'Info', 'Neutro', 'Destaque'], c => [prop(c, 'Tipo'), prop(c, 'Tom')], 16],
]) {
  const sec = page.findOne(n => n.type === 'SECTION' && n.name === nomeSecao);
  const set = sec.findOne(n => n.type === 'COMPONENT_SET');
  sec.children.filter(n => n.name.startsWith('Rótulos da grade')).forEach(n => n.remove());
  set.x = 200; set.y = 260;
  const g = grade(set, linhas, colunas, chave, gap);
  await rotular(sec, set, g, linhas, colunas); encaixar(sec);
}
// as seções seguintes não podem sobrepor Botão/Selo, que cresceram
const secs = page.children.filter(n => n.type === 'SECTION').sort((a, b) => a.y - b.y);
for (let i = 1; i < secs.length; i++) secs[i].y = Math.max(secs[i].y, secs[i - 1].y + secs[i - 1].height + 160);

// ---- P3.d Campo
const secCampo = await novaSecao('Campo', '.et-campo vai direto no input, select ou textarea: 48px, borda linha forte, raio de 12px. No foco, borda ouro escuro com halo dourado de 3px; inválido (aria-invalid) em vermelho; bloqueado com fundo de faixa. O erro é escrito ao lado do campo, não no topo do formulário.');
const estados = {
  'Padrão': { borda: 'cor/borda/forte', fundo: 'cor/campo/fundo', tinta: 'cor/texto/apagado', txt: 'Ex.: Plano anual' },
  'Preenchido': { borda: 'cor/borda/forte', fundo: 'cor/campo/fundo', tinta: 'cor/texto/padrao', txt: 'Plano trimestral' },
  'Foco': { borda: 'cor/borda/foco', fundo: 'cor/campo/fundo', tinta: 'cor/texto/padrao', txt: 'Plano trimestral', efeito: [sh(3, 0.961, 0.725, 0.078, 0.35)] },
  'Inválido': { borda: 'cor/situacao/perigo/borda', fundo: 'cor/campo/fundo', tinta: 'cor/texto/padrao', txt: '123', efeito: [sh(3, 0.627, 0.2, 0.145, 0.18)] },
  'Bloqueado': { borda: 'cor/borda/padrao', fundo: 'cor/campo/bloqueado', tinta: 'cor/texto/secundario', txt: '00012' },
};
const campos = [];
for (const [en, cfg] of Object.entries(estados)) {
  const c = figma.createComponent(); c.name = `Estado=${en}`;
  c.layoutMode = 'HORIZONTAL'; c.primaryAxisSizingMode = 'FIXED'; c.counterAxisSizingMode = 'FIXED'; c.counterAxisAlignItems = 'CENTER';
  c.resize(320, 48); c.setBoundVariable('height', D('altura/controle'));
  bind(c, ['paddingLeft', 'paddingRight'], D('espaco/4')); bind(c, RAIO, D('raio/botao'));
  c.fills = pintar(V(cfg.fundo)); c.strokes = pintar(V(cfg.borda)); c.strokeWeight = 1;
  if (cfg.efeito) c.effects = cfg.efeito;
  const t = await texto(c, cfg.txt, 'Corpo/MD', V(cfg.tinta)); t.name = 'valor'; t.layoutSizingHorizontal = 'FILL';
  campos.push(c);
}
const setCampo = figma.combineAsVariants(campos, secCampo); setCampo.name = 'Campo';
setCampo.description = 'Campo (.et-campo). Preenchido mostra o valor; Padrão mostra o placeholder em texto 3.';
const pValor = setCampo.addComponentProperty('Valor', 'TEXT', 'Plano trimestral');
for (const c of setCampo.children) { const t = c.findOne(n => n.name === 'valor'); const v = t.characters; t.componentPropertyReferences = { characters: pValor }; t.characters = v; }
setCampo.x = 200; setCampo.y = 220;
const gC = grade(setCampo, Object.keys(estados), ['x'], c => [prop(c, 'Estado'), 'x'], 20);
await rotular(secCampo, setCampo, gC, Object.keys(estados), []);
// Grupo de campo: rótulo + campo + ajuda
const grupo = figma.createComponent(); grupo.name = 'Grupo de campo';
grupo.layoutMode = 'VERTICAL'; grupo.primaryAxisSizingMode = 'AUTO'; grupo.counterAxisSizingMode = 'FIXED'; grupo.resize(320, 100);
bind(grupo, ['itemSpacing'], D('espaco/2')); grupo.fills = [];
const lab = await texto(grupo, 'Nome do plano', 'Corpo/SM Forte', V('cor/texto/padrao')); lab.name = 'rótulo';
const instCampo = setCampo.children.find(c => prop(c, 'Estado') === 'Padrão').createInstance(); grupo.appendChild(instCampo); instCampo.layoutSizingHorizontal = 'FILL';
instCampo.isExposedInstance = true;
const aj = await texto(grupo, 'Aparece para o aluno na hora de escolher o plano.', 'Corpo/XS', V('cor/texto/secundario')); aj.name = 'ajuda'; aj.layoutSizingHorizontal = 'FILL'; aj.textAutoResize = 'HEIGHT';
const pgR = grupo.addComponentProperty('Rótulo', 'TEXT', 'Nome do plano'), pgA = grupo.addComponentProperty('Ajuda', 'TEXT', 'Aparece para o aluno na hora de escolher o plano.'), pgM = grupo.addComponentProperty('Mostrar ajuda', 'BOOLEAN', true);
lab.componentPropertyReferences = { characters: pgR }; aj.componentPropertyReferences = { characters: pgA, visible: pgM };
grupo.description = 'Rótulo (14px, 600) + Campo + ajuda (13px). O erro substitui a ajuda, em vermelho, ao lado do campo.';
secCampo.appendChild(grupo); grupo.x = setCampo.x + setCampo.width + 80; grupo.y = setCampo.y;
encaixar(secCampo);

// ---- P3.e Caixa
const secCaixa = await novaSecao('Caixa e interruptor', 'Caixa (.et-caixa) para aceite, "lembrar meu usuário", ação ao salvar e chamada de presença. Interruptor (.et-interruptor, role="switch") para uma configuração que liga e desliga; sempre dentro da linha de 44px em que a linha inteira é o alvo de toque.');
const caixas = [];
for (const tipo of ['Checkbox', 'Radio']) for (const m of ['Não', 'Sim']) {
  const c = figma.createComponent(); c.name = `Tipo=${tipo}, Marcada=${m}`; c.resize(20, 20);
  if (tipo === 'Radio') c.cornerRadius = 10; else bind(c, RAIO, D('raio/selo'));
  c.strokeWeight = 1;
  if (m === 'Sim') {
    c.fills = pintar(V('cor/caixa/marcada')); c.strokes = pintar(V('cor/caixa/marcada'));
    if (tipo === 'Checkbox') { const i = icone('Check').createInstance(); c.appendChild(i); i.resize(14, 14); i.x = 3; i.y = 3; pintarIcone(i, V('cor/caixa/sinal')); }
    else { const p = figma.createEllipse(); p.name = 'ponto'; p.resize(6, 6); p.x = 7; p.y = 7; p.fills = pintar(V('cor/caixa/sinal')); c.appendChild(p); }
  } else { c.fills = pintar(V('cor/caixa/fundo')); c.strokes = pintar(V('cor/caixa/borda')); }
  caixas.push(c);
}
const setCaixa = figma.combineAsVariants(caixas, secCaixa); setCaixa.name = 'Caixa';
setCaixa.description = 'Checkbox e radio (.et-caixa): 20px, raio 6px; marcada em preto com sinal branco (no escuro, dourada com sinal preto).';
setCaixa.x = 200; setCaixa.y = 240;
const gCx = grade(setCaixa, ['Checkbox', 'Radio'], ['Não', 'Sim'], c => [prop(c, 'Tipo'), prop(c, 'Marcada')], 24);
await rotular(secCaixa, setCaixa, gCx, ['Checkbox', 'Radio'], ['Não', 'Sim']);

// ---- P3.f Interruptor
const inters = [];
for (const sup of ['Claro', 'Escuro']) for (const lig of ['Não', 'Sim']) {
  const X = sup === 'Escuro' ? VE : (n => V(n));
  const c = figma.createComponent(); c.name = `Ligado=${lig}, Superfície=${sup}`; c.resize(44, 24);
  bind(c, RAIO, D('raio/pilula')); c.strokeWeight = 1;
  c.fills = pintar(X(lig === 'Sim' ? 'cor/interruptor/ligado' : 'cor/interruptor/trilho'));
  c.strokes = pintar(X(lig === 'Sim' ? 'cor/interruptor/ligado' : 'cor/interruptor/borda'));
  const p = figma.createEllipse(); p.name = 'polegar'; p.resize(18, 18); p.y = 3; p.x = lig === 'Sim' ? 23 : 3;
  p.fills = pintar(X(lig === 'Sim' ? 'cor/interruptor/polegar-ligado' : 'cor/interruptor/polegar'));
  if (lig === 'Não' && sup === 'Claro') { p.strokes = pintar(X('cor/interruptor/polegar-borda')); p.strokeWeight = 1; }
  p.effects = [{ type: 'DROP_SHADOW', color: { r: 0.1, g: 0.086, b: 0.039, a: 0.2 }, offset: { x: 0, y: 1 }, radius: 2, spread: 0, visible: true, blendMode: 'NORMAL' }];
  c.appendChild(p); inters.push(c);
}
const setInter = figma.combineAsVariants(inters, secCaixa); setInter.name = 'Interruptor';
setInter.description = 'Switch (.et-interruptor): trilho 44×24. Desligado: trilho claro e polegar branco contornado. Ligado: trilho preto e polegar dourado. No escuro: trilho dourado e polegar preto.';
setInter.x = setCaixa.x + setCaixa.width + 200; setInter.y = 240;
const gI = grade(setInter, ['Claro', 'Escuro'], ['Não', 'Sim'], c => [prop(c, 'Superfície'), prop(c, 'Ligado')], 24);
// fundo escuro atrás da linha Escuro
const faixa = figma.createRectangle(); faixa.name = 'fundo escuro (referência)'; secCaixa.appendChild(faixa);
faixa.x = setInter.x + 12; faixa.y = setInter.y + gI.ys['Escuro'] - 12; faixa.resize(setInter.width - 24, gI.alt['Escuro'] + 24);
faixa.fills = pintar(V('cor/fundo/palco')); bind(faixa, RAIO, D('raio/botao'));
secCaixa.insertChild(secCaixa.children.indexOf(setInter), faixa);
setInter.fills = []; setInter.strokes = pintar(V('cor/borda/padrao')); setInter.dashPattern = [6, 4];
await rotular(secCaixa, setInter, gI, ['Claro', 'Escuro'], ['Não', 'Sim']);

// Linha do interruptor
const linhas = [];
for (const sup of ['Claro', 'Escuro']) {
  const X = sup === 'Escuro' ? VE : (n => V(n));
  const c = figma.createComponent(); c.name = `Superfície=${sup}`;
  c.layoutMode = 'HORIZONTAL'; c.primaryAxisSizingMode = 'FIXED'; c.counterAxisSizingMode = 'AUTO'; c.resize(360, 44);
  c.counterAxisAlignItems = 'MIN'; bind(c, ['itemSpacing'], D('espaco/3')); bind(c, ['paddingTop', 'paddingBottom'], D('espaco/2'));
  c.minHeight = 44; c.setBoundVariable('minHeight', D('altura/alvo-toque'));
  c.fills = sup === 'Escuro' ? pintar(V('cor/fundo/palco')) : [];
  if (sup === 'Escuro') bind(c, ['paddingLeft', 'paddingRight'], D('espaco/3'));
  const ins = setInter.children.find(k => prop(k, 'Superfície') === sup && prop(k, 'Ligado') === 'Sim').createInstance(); ins.name = 'interruptor'; c.appendChild(ins); ins.isExposedInstance = true;
  const col2 = figma.createAutoLayout('VERTICAL', { name: 'texto' }); c.appendChild(col2); col2.fills = []; col2.itemSpacing = 2; col2.layoutSizingHorizontal = 'FILL';
  const r = await texto(col2, 'Exibir WhatsApp no site', 'Corpo/SM Forte', X('cor/texto/padrao')); r.name = 'rótulo'; r.layoutSizingHorizontal = 'FILL'; r.textAutoResize = 'HEIGHT';
  const a = await texto(col2, 'O número aparece no perfil público do professor.', 'Corpo/XS', X('cor/texto/secundario')); a.name = 'ajuda'; a.layoutSizingHorizontal = 'FILL'; a.textAutoResize = 'HEIGHT';
  linhas.push(c);
}
const setLinha = figma.combineAsVariants(linhas, secCaixa); setLinha.name = 'Linha do interruptor';
setLinha.description = '<label class="et-interruptor-linha">: interruptor antes do rótulo, a linha inteira (mín. 44px) é o alvo de toque. Macro interruptor() em components/ui.html; o nome acessível é só o rótulo e a ajuda vira descrição.';
const plR = setLinha.addComponentProperty('Rótulo', 'TEXT', 'Exibir WhatsApp no site'), plA = setLinha.addComponentProperty('Ajuda', 'TEXT', 'O número aparece no perfil público do professor.'), plM = setLinha.addComponentProperty('Mostrar ajuda', 'BOOLEAN', true);
for (const c of setLinha.children) { c.findOne(n => n.name === 'rótulo').componentPropertyReferences = { characters: plR }; c.findOne(n => n.name === 'ajuda').componentPropertyReferences = { characters: plA, visible: plM }; }
setLinha.layoutMode = 'VERTICAL'; setLinha.primaryAxisSizingMode = 'AUTO'; setLinha.counterAxisSizingMode = 'AUTO'; setLinha.itemSpacing = 16; bind(setLinha, PAD, D('espaco/6')); moldura(setLinha);
setLinha.x = setInter.x + setInter.width + 120; setLinha.y = 240;
encaixar(secCaixa);

// ---- P3.g Aviso
const secAviso = await novaSecao('Aviso', '.et-aviso (role="alert"): raio de 12px, texto de 14px. O ícone fica na margem esquerda. Erros dizem o que aconteceu e como resolver, sem pedir desculpa.');
const tonsA = { 'Neutro': [null, 'Info', 'Use a busca para encontrar um aluno pelo nome ou CPF.'], 'Ok': ['ok', 'Check', 'E-mail verificado. Seu cadastro foi enviado para análise.'], 'Alerta': ['alerta', 'Alerta', 'Sua mensalidade vence em 3 dias. Pague pelo Pix na área do aluno.'], 'Perigo': ['perigo', 'Alerta', 'Link inválido ou expirado. Peça um novo na tela de recuperar senha.'], 'Info': ['info', 'Info', 'O Mercado Pago ainda está processando este pagamento.'] };
const avisos = [];
for (const [tn, [k, ic, txt]] of Object.entries(tonsA)) {
  const c = figma.createComponent(); c.name = `Tom=${tn}`;
  c.layoutMode = 'HORIZONTAL'; c.primaryAxisSizingMode = 'FIXED'; c.counterAxisSizingMode = 'AUTO'; c.resize(480, 44);
  bind(c, ['paddingTop', 'paddingBottom'], D('espaco/3')); bind(c, ['paddingLeft', 'paddingRight'], D('espaco/4')); bind(c, ['itemSpacing'], D('espaco/3')); bind(c, RAIO, D('raio/botao'));
  const tinta = k ? V(`cor/situacao/${k}/tinta`) : V('cor/texto/padrao');
  c.fills = pintar(k ? V(`cor/situacao/${k}/fundo`) : V('cor/fundo/superficie'));
  c.strokes = k ? pintar(V(`cor/situacao/${k}/borda`), 0.35) : pintar(V('cor/borda/forte')); c.strokeWeight = 1;
  const i = icone(ic).createInstance(); i.name = 'ícone'; c.appendChild(i); i.resize(18, 18); pintarIcone(i, tinta);
  const t = await texto(c, txt, 'Corpo/SM', tinta); t.name = 'texto'; t.layoutSizingHorizontal = 'FILL'; t.textAutoResize = 'HEIGHT';
  avisos.push(c);
}
const setAviso = figma.combineAsVariants(avisos, secAviso); setAviso.name = 'Aviso';
setAviso.description = 'Alerta (.et-aviso--<tom>). No .auth-shell e no .et-escuro, usa as versões escuras dos tons.';
const paT = setAviso.addComponentProperty('Texto', 'TEXT', 'Sua mensalidade vence em 3 dias.'), paM = setAviso.addComponentProperty('Mostrar ícone', 'BOOLEAN', true), paI = setAviso.addComponentProperty('Ícone', 'INSTANCE_SWAP', icone('Info').id);
for (const c of setAviso.children) { const t = c.findOne(n => n.name === 'texto'); const v = t.characters; t.componentPropertyReferences = { characters: paT }; t.characters = v; c.findOne(n => n.name === 'ícone').componentPropertyReferences = { visible: paM, mainComponent: paI }; }
setAviso.x = 200; setAviso.y = 220;
const gA = grade(setAviso, Object.keys(tonsA), ['x'], c => [prop(c, 'Tom'), 'x'], 16);
await rotular(secAviso, setAviso, gA, Object.keys(tonsA), []);
encaixar(secAviso);

return {
  campo: { id: setCampo.id, n: setCampo.children.length, grupo: grupo.id },
  caixa: { id: setCaixa.id, n: setCaixa.children.length },
  interruptor: { id: setInter.id, n: setInter.children.length, linha: setLinha.id, nLinha: setLinha.children.length },
  aviso: { id: setAviso.id, n: setAviso.children.length },
  secoes: page.children.filter(n => n.type === 'SECTION').map(s => ({ id: s.id, nome: s.name, y: Math.round(s.y), h: Math.round(s.height) })),
};
