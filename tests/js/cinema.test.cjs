// Hero cinematográfico (static/js/cinema.js): a rolagem dentro da seção vira o
// progresso de 0 a 1, troca a manchete ativa (as outras saem do leitor de tela e da
// ordem do Tab), enche o medidor e publica o estado para a cena 3D. Sem condição de
// ter 3D, nada é importado e o loader sai assim que a página fica pronta.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const CODIGO = fs.readFileSync(path.join(__dirname, '../../static/js/cinema.js'), 'utf8');

class ListaDeClasses {
    constructor() { this.itens = new Set(); }
    add(classe) { this.itens.add(classe); }
    remove(classe) { this.itens.delete(classe); }
    contains(classe) { return this.itens.has(classe); }
    toggle(classe, ligar) { if (ligar) this.itens.add(classe); else this.itens.delete(classe); }
}

class Elemento {
    constructor() {
        this.classList = new ListaDeClasses();
        this.atributos = new Map();
        this.style = {};
        this.inert = false;
        this.textContent = '';
    }
    setAttribute(nome, valor) { this.atributos.set(nome, String(valor)); }
    removeAttribute(nome) { this.atributos.delete(nome); }
    getAttribute(nome) { return this.atributos.has(nome) ? this.atributos.get(nome) : null; }
}

// Seção de 3600px numa janela de 900px: o percurso da rolagem é de 2700px.
function montar({ reduzir = false, webgl = false } = {}) {
    const manchetes = [0, 1, 2, 3].map(() => new Elemento());
    const preenchimento = new Elemento();
    const valor = new Elemento();
    const alvoCena = new Elemento();
    const carregando = new Elemento();
    const secao = new Elemento();
    const caixa = { top: 0, height: 3600 };
    secao.getBoundingClientRect = () => caixa;
    secao.querySelectorAll = (seletor) => (seletor === '[data-cinema-manchete]' ? manchetes : []);
    secao.querySelector = (seletor) => ({
        '[data-cinema-medidor-preenchimento]': preenchimento,
        '[data-cinema-medidor-valor]': valor,
        '[data-cinema-cena]': alvoCena,
    })[seletor] || null;
    secao.setAttribute('data-cena-src', '/static/dist/cinema/cena-teste.js');

    const ouvintes = {};
    const quadros = [];
    const eventos = [];
    const armazenado = new Map();
    const contextosWebgl = [];
    const window = {
        innerHeight: 900,
        matchMedia: (consulta) => ({ matches: consulta.includes('reduce') ? reduzir : false }),
        addEventListener: (nome, funcao) => { (ouvintes[nome] = ouvintes[nome] || []).push(funcao); },
        requestAnimationFrame: (funcao) => { quadros.push(funcao); return quadros.length; },
        dispatchEvent: (evento) => { eventos.push(evento); },
        requestIdleCallback: (funcao) => funcao(),
    };
    const document = {
        readyState: 'complete',
        fonts: { ready: Promise.resolve() },
        querySelector: (seletor) => ({ '[data-cinema]': secao, '[data-cinema-carregando]': carregando })[seletor] || null,
        createElement: () => ({
            getContext: () => {
                if (!webgl) return null;
                const contexto = { perdido: false, getExtension: () => ({ loseContext() { contexto.perdido = true; } }) };
                contextosWebgl.push(contexto);
                return contexto;
            },
        }),
    };
    class CustomEvent {
        constructor(tipo, inicial) { this.type = tipo; this.detail = inicial.detail; }
    }
    vm.runInNewContext(CODIGO, {
        window, document, CustomEvent, navigator: {},
        sessionStorage: { setItem: (chave, v) => armazenado.set(chave, v) },
        setTimeout: () => 0,
    });

    return {
        window, secao, manchetes, preenchimento, valor, carregando, eventos, armazenado, contextosWebgl,
        rolarAte(fracao) {
            caixa.top = -2700 * fracao;
            ouvintes.scroll.forEach((funcao) => funcao());
            while (quadros.length) quadros.shift()();
        },
    };
}

const esperarPromessas = () => new Promise((resolver) => setImmediate(resolver));

function conferirAtiva(hero, ativa) {
    hero.manchetes.forEach((manchete, i) => {
        assert.equal(manchete.classList.contains('is-active'), i === ativa, `is-active da manchete ${i}`);
        assert.equal(manchete.classList.contains('is-before'), i < ativa, `is-before da manchete ${i}`);
        assert.equal(manchete.classList.contains('is-after'), i > ativa, `is-after da manchete ${i}`);
        // "true" de verdade: aria-hidden="" não esconde nada do leitor de tela.
        assert.equal(manchete.getAttribute('aria-hidden'), i === ativa ? null : 'true');
        assert.equal(manchete.inert, i !== ativa);
    });
}

test('no topo, a primeira manchete é a ativa e o medidor marca 00', () => {
    const hero = montar();
    assert.equal(hero.window.etCinema.progresso, 0);
    assert.equal(hero.window.etCinema.indice, 0);
    assert.equal(hero.valor.textContent, '00');
    assert.equal(hero.preenchimento.style.transform, 'scaleY(0.0400)');
});

test('a rolagem troca a manchete, enche o medidor e publica o progresso', () => {
    const hero = montar();
    hero.rolarAte(0.55);
    assert.equal(hero.window.etCinema.indice, 2);
    assert.ok(Math.abs(hero.window.etCinema.progresso - 0.55) < 1e-9);
    conferirAtiva(hero, 2);
    assert.equal(hero.valor.textContent, '55');
    assert.equal(hero.preenchimento.style.transform, 'scaleY(0.5500)');
    const ultimo = hero.eventos.at(-1);
    assert.equal(ultimo.type, 'cinema:progresso');
    assert.equal(ultimo.detail.indice, 2);
});

test('depois do fim da pista, fica na última manchete com 100', () => {
    const hero = montar();
    hero.rolarAte(1.8);
    assert.equal(hero.window.etCinema.progresso, 1);
    conferirAtiva(hero, 3);
    assert.equal(hero.valor.textContent, '100');
});

test('voltar ao topo devolve a primeira manchete', () => {
    const hero = montar();
    hero.rolarAte(0.9);
    hero.rolarAte(0);
    conferirAtiva(hero, 0);
});

test('com movimento reduzido nada de WebGL é testado e o loader sai', async () => {
    const hero = montar({ reduzir: true, webgl: true });
    await esperarPromessas();
    await esperarPromessas();
    assert.equal(hero.contextosWebgl.length, 0);
    assert.ok(hero.carregando.classList.contains('is-complete'));
    assert.ok(hero.secao.classList.contains('cinema--pronto'));
    assert.ok(!hero.secao.classList.contains('cinema--cena-pronta'));
    assert.equal(hero.armazenado.get('et-cinema-visto'), '1');
});

test('sem WebGL a cena não é importada e o loader sai do mesmo jeito', async () => {
    const hero = montar({ webgl: false });
    await esperarPromessas();
    await esperarPromessas();
    assert.ok(hero.carregando.classList.contains('is-complete'));
    assert.ok(!hero.secao.classList.contains('cinema--cena-pronta'));
});
