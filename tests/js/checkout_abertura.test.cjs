const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const flush = () => new Promise((resolve) => setImmediate(resolve));

function criarPagina({ action = '/checkout/mensalidade/42', respeitarAbort = true } = {}) {
    function elemento() {
        const eventos = new Map();
        const atributos = new Map();
        return {
            childNodes: [], dataset: {}, disabled: false, hidden: false,
            get textContent() { return this.childNodes.map((node) => node.textContent).join(''); },
            set textContent(texto) { this.childNodes = [{ textContent: texto }]; },
            append(...nodes) { this.childNodes.push(...nodes); },
            replaceChildren(...nodes) { this.childNodes = nodes; },
            setAttribute(nome, valor) { atributos.set(nome, valor); },
            getAttribute(nome) { return atributos.get(nome); },
            removeAttribute(nome) { atributos.delete(nome); },
            addEventListener(nome, callback) {
                if (!eventos.has(nome)) eventos.set(nome, []);
                eventos.get(nome).push(callback);
            },
            emitir(nome, evento = {}) {
                for (const callback of eventos.get(nome) || []) callback(evento);
            },
        };
    }

    const form = elemento();
    form.action = action;
    form.campos = [['csrf_token', 'csrf-existente']];
    form.closest = (seletor) => seletor === '.form-outras-formas' ? form : null;
    const botao = elemento();
    const icone = { textContent: '', tagName: 'svg' };
    const rotulo = { textContent: 'Outras formas de pagamento', tagName: 'span' };
    botao.append(icone, rotulo);
    form.append(botao);
    form.querySelector = (seletor) => seletor === '[data-checkout-abrir]' ? botao : null;

    const document = elemento();
    document.createElement = () => elemento();
    document.getElementById = () => null;
    document.querySelectorAll = (seletor) => seletor === '.form-outras-formas' ? [form] : [];
    const window = elemento();
    const navegacoes = [];
    window.location = {
        href: 'https://academia.example/perfil', origin: 'https://academia.example',
        assign(url) { navegacoes.push(url); },
    };
    const timers = new Map();
    const pedidos = [];
    let proximoTimer = 0;
    const contexto = {
        document, window, URL, AbortController, Error, TypeError, SyntaxError,
        FormData: class {
            constructor(formulario) { this.campos = formulario.campos; }
            entries() { return this.campos.values(); }
        },
        setTimeout(callback, tempo) {
            const id = ++proximoTimer;
            timers.set(id, { callback, tempo });
            return id;
        },
        clearTimeout(id) { timers.delete(id); },
        fetch(url, opcoes) {
            return new Promise((resolve, reject) => {
                pedidos.push({ url, opcoes, resolve, reject });
                if (respeitarAbort) {
                    opcoes.signal.addEventListener('abort', () => reject(new DOMException('Cancelado', 'AbortError')));
                }
            });
        },
    };
    const arquivo = path.resolve(__dirname, '../../static/js/checkout.js');
    vm.runInNewContext(fs.readFileSync(arquivo, 'utf8'), contexto, { filename: arquivo });

    return {
        form, botao, icone, rotulo, pedidos, navegacoes, timers, window,
        get erro() { return form.childNodes.find((node) => node.getAttribute?.('role') === 'alert'); },
        enviar() {
            const evento = { target: form, defaultPrevented: false, preventDefault() { this.defaultPrevented = true; } };
            document.emitir('submit', evento);
            assert.equal(evento.defaultPrevented, true, 'o POST nativo não pode seguir redirecionamento externo');
        },
        async responder(dados, { indice = 0, status = 200, tipo = 'application/json', json } = {}) {
            pedidos[indice].resolve({
                ok: status >= 200 && status < 300, status,
                headers: { get: () => tipo },
                json: json || (async () => dados),
            });
            await flush();
        },
        async expirar() {
            for (const { callback, tempo } of [...timers.values()]) {
                assert.equal(tempo, 15000);
                callback();
            }
            await flush();
        },
    };
}

test('checkout: envia apenas os campos do formulário para same-origin e navega por GET', async () => {
    const pagina = criarPagina();
    pagina.enviar();
    assert.equal(pagina.botao.disabled, true);
    assert.equal(pagina.botao.textContent, 'Abrindo checkout…');
    assert.equal(pagina.form.getAttribute('aria-busy'), 'true');
    const { url, opcoes } = pagina.pedidos[0];
    assert.equal(url, 'https://academia.example/checkout/mensalidade/42');
    assert.equal(opcoes.method, 'POST');
    assert.equal(opcoes.redirect, 'error');
    assert.equal(opcoes.credentials, 'same-origin');
    assert.equal(opcoes.mode, 'same-origin');
    assert.equal(opcoes.headers.Accept, 'application/json');
    assert.deepEqual([...opcoes.body.entries()], [['csrf_token', 'csrf-existente']]);
    await pagina.responder({ url_checkout: 'https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=exemplo' });
    assert.deepEqual(pagina.navegacoes, ['https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=exemplo']);
    assert.equal(pagina.pedidos.length, 1, 'fetch nunca acessa o provedor externo');
    assert.equal(pagina.timers.size, 0);
    assert.equal(pagina.botao.disabled, false);
    assert.equal(pagina.erro.hidden, true);
    assert.strictEqual(pagina.botao.childNodes[0], pagina.icone, 'o ícone original é preservado');
    assert.strictEqual(pagina.botao.childNodes[1], pagina.rotulo);
});

test('checkout: clique duplo faz somente um pedido', async () => {
    const pagina = criarPagina();
    pagina.enviar();
    pagina.enviar();
    assert.equal(pagina.pedidos.length, 1);
    await pagina.responder({ url_checkout: 'https://sandbox.mercadopago.com.br/checkout/v1/redirect?pref_id=teste' });
    assert.equal(pagina.navegacoes.length, 1);
});

test('checkout: timeout cancela, restaura o botão e ignora a resposta antiga ao tentar novamente', async () => {
    const pagina = criarPagina({ respeitarAbort: false });
    pagina.enviar();
    await pagina.expirar();
    assert.equal(pagina.pedidos[0].opcoes.signal.aborted, true);
    assert.equal(pagina.botao.disabled, false);
    assert.equal(pagina.erro.hidden, false);
    assert.match(pagina.erro.textContent, /demorou/);
    assert.equal(pagina.form.getAttribute('aria-busy'), undefined);
    pagina.enviar();
    assert.equal(pagina.erro.hidden, true);
    await pagina.responder({ url_checkout: 'https://www.mercadopago.com.br/antigo' });
    assert.equal(pagina.navegacoes.length, 0);
    assert.equal(pagina.botao.disabled, true, 'a resposta antiga não restaura o pedido novo');
    await pagina.responder({ url_checkout: 'https://www.mercadopago.com.br/novo' }, { indice: 1 });
    assert.deepEqual(pagina.navegacoes, ['https://www.mercadopago.com.br/novo']);
});

for (const [nome, dados, opcoes, mensagem] of [
    ['erro do provedor', { erro: 'O provedor está indisponível. Tente novamente.' }, { status: 503 }, /provedor está indisponível/],
    ['sessão expirada', null, { status: 401, tipo: 'text/html' }, /sessão expirou/],
    ['CSRF expirado', null, { status: 400, tipo: 'text/html' }, /validar o formulário.*Recarregue/],
    ['erro HTML do servidor', null, { status: 500, tipo: 'text/html' }, /Não foi possível abrir/],
    ['HTML inesperado', null, { status: 200, tipo: 'text/html' }, /Não foi possível abrir/],
    ['JSON malformado', null, { json: async () => { throw new SyntaxError('JSON inválido'); } }, /Não foi possível conectar/],
]) {
    test(`checkout: ${nome} exibe mensagem e permite tentar novamente`, async () => {
        const pagina = criarPagina();
        pagina.enviar();
        await pagina.responder(dados, opcoes);
        assert.equal(pagina.botao.disabled, false);
        assert.equal(pagina.botao.textContent, 'Outras formas de pagamento');
        assert.equal(pagina.erro.hidden, false);
        assert.match(pagina.erro.textContent, mensagem);
        assert.equal(pagina.timers.size, 0);
        assert.equal(pagina.navegacoes.length, 0);
    });
}

test('checkout: falha de rede ou redirecionamento HTTP inesperado não deixa botão travado', async () => {
    const pagina = criarPagina();
    pagina.enviar();
    pagina.pedidos[0].reject(new TypeError('Failed to fetch'));
    await flush();
    assert.equal(pagina.botao.disabled, false);
    assert.match(pagina.erro.textContent, /Não foi possível conectar/);
    assert.equal(pagina.navegacoes.length, 0);
});

test('checkout: erro retornado é texto, sem interpretar HTML', async () => {
    const pagina = criarPagina();
    pagina.enviar();
    const erro = '<script>alert(1)</script>';
    await pagina.responder({ erro }, { status: 400 });
    assert.equal(pagina.erro.textContent, erro);
    assert.equal(pagina.erro.childNodes.length, 1);
    assert.equal(pagina.erro.childNodes[0].tagName, undefined);
});

test('checkout: rejeita URLs externas, HTTP, credenciais, portas e respostas incompletas', async () => {
    for (const url_checkout of [
        'https://mercadopago.com.br.attacker.example/checkout',
        'https://attacker.example/checkout',
        'http://www.mercadopago.com.br/checkout',
        'javascript:alert(1)',
        'https://user:password@www.mercadopago.com.br/checkout',
        'https://www.mercadopago.com.br:8443/checkout',
        '/checkout/relativo', null,
    ]) {
        const pagina = criarPagina();
        pagina.enviar();
        await pagina.responder({ url_checkout });
        assert.equal(pagina.navegacoes.length, 0, String(url_checkout));
        assert.equal(pagina.botao.disabled, false);
        assert.equal(pagina.erro.hidden, false);
    }
});

test('checkout: nunca envia formulário para outra origem', async () => {
    const pagina = criarPagina({ action: 'https://attacker.example/checkout' });
    pagina.enviar();
    await flush();
    assert.equal(pagina.pedidos.length, 0);
    assert.equal(pagina.botao.disabled, false);
    assert.match(pagina.erro.textContent, /Destino de pagamento inválido/);
});

test('checkout: sair e voltar pelo bfcache restaura ícones e ignora a resposta cancelada', async () => {
    const pagina = criarPagina({ respeitarAbort: false });
    pagina.enviar();
    pagina.window.emitir('pagehide');
    assert.equal(pagina.pedidos[0].opcoes.signal.aborted, true);
    assert.equal(pagina.timers.size, 0);
    assert.equal(pagina.botao.disabled, false);
    assert.strictEqual(pagina.botao.childNodes[0], pagina.icone);
    pagina.window.emitir('pageshow', { persisted: true });
    await pagina.responder({ url_checkout: 'https://www.mercadopago.com.br/checkout' });
    assert.equal(pagina.navegacoes.length, 0);
    assert.equal(pagina.erro.hidden, true);
    pagina.enviar();
    assert.equal(pagina.pedidos.length, 2);
});

test('checkout: timeout também cobre leitura lenta da resposta JSON', async () => {
    const pagina = criarPagina();
    pagina.enviar();
    let concluirJSON;
    await pagina.responder(null, { json: () => new Promise((resolve) => { concluirJSON = resolve; }) });
    await pagina.expirar();
    concluirJSON({ url_checkout: 'https://www.mercadopago.com.br/checkout' });
    await flush();
    assert.equal(pagina.navegacoes.length, 0);
    assert.equal(pagina.botao.disabled, false);
    assert.match(pagina.erro.textContent, /demorou/);
});
