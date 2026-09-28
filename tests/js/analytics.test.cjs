// Consentimento do GA4 (static/js/analytics.js): nada vai para o Google antes do
// "Aceitar", o endereço sai sem query string e recusar apaga os cookies _ga.
// Nenhum pedido sai para a rede: o <script> do gtag só é registrado, nunca executado.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const CODIGO = fs.readFileSync(path.join(__dirname, '../../static/js/analytics.js'), 'utf8');
const ID = 'G-TESTE12345';

class Element {
    constructor(atributo) { this.atributo = atributo; }
    closest(seletor) { return seletor === `[${this.atributo}]` ? this : null; }
}

function montar({ escolha = null, evento = '', referrer = '', localStorageQuebrado = false } = {}) {
    const armazenado = new Map();
    if (escolha) armazenado.set('et-consentimento-analytics', JSON.stringify({ versao: 1, escolha }));
    const scripts = [];
    const cliques = [];
    const cookiesEscritos = [];
    let cookieAtual = '_ga=GA1.1.123; _ga_TESTE12345=GS1.1.456; sessao=abc';
    const botao = { focado: false, focus() { this.focado = true; } };
    const banner = { hidden: true, querySelector: () => botao };

    const document = {
        currentScript: { dataset: { analyticsId: ID, evento } },
        referrer,
        head: { appendChild: (el) => scripts.push(el) },
        querySelector: (seletor) => (seletor === '[data-consentimento]' ? banner : null),
        createElement: () => ({}),
        addEventListener: (nome, callback) => { if (nome === 'click') cliques.push(callback); },
        get cookie() { return cookieAtual; },
        set cookie(valor) { cookiesEscritos.push(valor); },
    };
    const localStorage = {
        getItem(chave) {
            if (localStorageQuebrado) throw new Error('SecurityError');
            return armazenado.has(chave) ? armazenado.get(chave) : null;
        },
        setItem(chave, valor) {
            if (localStorageQuebrado) throw new Error('SecurityError');
            armazenado.set(chave, valor);
        },
    };
    const window = {
        localStorage,
        location: {
            origin: 'https://academia.example.test',
            pathname: '/cadastro/obrigado',
            search: '?token=segredo&email=pessoa@example.com',
            hostname: 'www.academia.example.test',
        },
    };
    vm.runInNewContext(CODIGO, { window, document, Element, URL });

    return {
        window, banner, botao, scripts, cookiesEscritos, armazenado,
        clicar(atributo) { cliques.forEach((cb) => cb({ target: new Element(atributo) })); },
        // JSON tira os objetos do contexto do vm (outro "realm") para o deepEqual comparar.
        chamadas() { return JSON.parse(JSON.stringify((window.dataLayer || []).map((args) => Array.from(args)))); },
    };
}

test('sem escolha: mostra o aviso e não carrega nada do Google', () => {
    const t = montar();
    assert.equal(t.banner.hidden, false);
    assert.equal(t.botao.focado, false);
    assert.equal(t.scripts.length, 0);
    assert.equal(t.window.dataLayer, undefined);
});

test('aceitar grava a escolha, esconde o aviso e só então baixa o gtag.js', () => {
    const t = montar();
    t.clicar('data-consentimento-aceitar');
    assert.equal(t.banner.hidden, true);
    assert.equal(JSON.parse(t.armazenado.get('et-consentimento-analytics')).escolha, 'aceito');
    assert.equal(t.scripts.length, 1);
    assert.equal(t.scripts[0].src, `https://www.googletagmanager.com/gtag/js?id=${ID}`);
});

test('endereço vai sem query string e a origem só com o domínio', () => {
    const t = montar({ escolha: 'aceito', referrer: 'https://academia.example.test/recuperar_senha/token-secreto?x=1' });
    const [, , opcoes] = t.chamadas().find(([tipo]) => tipo === 'config');
    assert.equal(opcoes.page_location, 'https://academia.example.test/cadastro/obrigado');
    assert.equal(opcoes.page_referrer, 'https://academia.example.test/');
    assert.equal(opcoes.allow_google_signals, false);
    assert.equal(opcoes.allow_ad_personalization_signals, false);
    const tudo = JSON.stringify(t.chamadas());
    assert.ok(!tudo.includes('token'));
    assert.ok(!tudo.includes('pessoa@example.com'));
});

test('publicidade fica negada mesmo com o aceite', () => {
    const t = montar({ escolha: 'aceito' });
    const [, , consentimento] = t.chamadas().find(([tipo, acao]) => tipo === 'consent' && acao === 'default');
    assert.deepEqual(consentimento, {
        analytics_storage: 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied',
    });
});

test('evento de conversão sai só com o aceite e sem parâmetro pessoal', () => {
    const recusado = montar({ escolha: 'recusado', evento: 'sign_up' });
    assert.equal(recusado.window.dataLayer, undefined);

    const t = montar({ evento: 'sign_up' });
    assert.equal(t.window.dataLayer, undefined);
    t.clicar('data-consentimento-aceitar');
    const eventos = t.chamadas().filter(([tipo]) => tipo === 'event');
    assert.deepEqual(eventos, [['event', 'sign_up', { method: 'site' }]]);
});

test('escolha "recusado" guardada: sem aviso e sem carregar', () => {
    const t = montar({ escolha: 'recusado' });
    assert.equal(t.banner.hidden, true);
    assert.equal(t.scripts.length, 0);
});

test('recusar depois de aceitar desliga a coleta e apaga os cookies _ga', () => {
    const t = montar({ escolha: 'aceito' });
    t.clicar('data-consentimento-abrir');
    assert.equal(t.banner.hidden, false);
    assert.equal(t.botao.focado, true);

    t.clicar('data-consentimento-recusar');
    assert.equal(t.window[`ga-disable-${ID}`], true);
    assert.deepEqual(t.chamadas().at(-1), ['consent', 'update', { analytics_storage: 'denied' }]);
    const apagados = t.cookiesEscritos.filter((c) => c.includes('Max-Age=0'));
    assert.ok(apagados.some((c) => c.startsWith('_ga=') && c.includes('domain=.academia.example.test')));
    assert.ok(apagados.some((c) => c.startsWith('_ga_TESTE12345=')));
    assert.ok(!apagados.some((c) => c.startsWith('sessao=')));

    // Mudou de ideia de novo na mesma página: volta a coletar sem baixar o gtag outra vez.
    t.clicar('data-consentimento-aceitar');
    assert.equal(t.window[`ga-disable-${ID}`], false);
    assert.deepEqual(t.chamadas().at(-1), ['consent', 'update', { analytics_storage: 'granted' }]);
    assert.equal(t.scripts.length, 1);
});

test('sem localStorage (aba anônima): o aviso aparece e o aceite vale para a página', () => {
    const t = montar({ localStorageQuebrado: true });
    assert.equal(t.banner.hidden, false);
    t.clicar('data-consentimento-aceitar');
    assert.equal(t.scripts.length, 1);
});
