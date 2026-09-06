// Estado de espera dos botões que dependem do Mercado Pago: trava, avisa por
// aria-busy e devolve o rótulo original em qualquer saída. Nenhum pedido sai
// para a rede: o fetch é controlado aqui dentro.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const flush = () => new Promise((resolve) => setImmediate(resolve));

function criarElemento(dataset = {}) {
    const eventos = new Map();
    const filhos = new Map();
    const atributos = new Map();
    return {
        dataset, textContent: '', value: '', hidden: false, open: false, disabled: false,
        atributos,
        classList: { add() {}, remove() {} },
        addEventListener(nome, callback) {
            if (!eventos.has(nome)) eventos.set(nome, []);
            eventos.get(nome).push(callback);
        },
        emitir(nome, evento = {}) {
            for (const callback of eventos.get(nome) || []) callback(evento);
        },
        querySelector(seletor) {
            if (seletor === '[data-rotulo]') return null;
            if (!filhos.has(seletor)) filhos.set(seletor, criarElemento());
            return filhos.get(seletor);
        },
        querySelectorAll() { return []; },
        showModal() { this.open = true; },
        close() { this.open = false; },
        setAttribute(nome, valor) { atributos.set(nome, String(valor)); },
        getAttribute(nome) { return atributos.has(nome) ? atributos.get(nome) : null; },
        removeAttribute(nome) { atributos.delete(nome); },
        focus() {},
    };
}

const ocupado = (botao) => botao.disabled === true
    && botao.dataset.ocupado === 'true'
    && botao.getAttribute('aria-busy') === 'true';

const livre = (botao) => botao.disabled === false
    && !botao.dataset.ocupado
    && botao.getAttribute('aria-busy') === null;

// Monta o ambiente e devolve o controle do fetch para o teste decidir quando
// (e como) a resposta chega.
function montar(script, { raizDataset, extras = {} } = {}) {
    const raiz = criarElemento(raizDataset);
    const document = criarElemento();
    const window = criarElemento();
    window.location = { reload() {}, assign() {} };
    const ids = { pagamento: 'pagina-pagamento', pix: 'pix-dialog' };
    document.getElementById = (id) => (id === ids[script] ? raiz : null);
    Object.assign(raiz, extras);

    const pedidos = [];
    const contexto = {
        document, window, Intl, console,
        setInterval() { return 1; },
        clearInterval() {},
        setTimeout() { return 1; },
        fetch(url, opcoes) {
            return new Promise((resolve, reject) => pedidos.push({ url, opcoes, resolve, reject }));
        },
    };
    const arquivo = path.resolve(__dirname, '../../static/js', `${script}.js`);
    vm.runInNewContext(fs.readFileSync(arquivo, 'utf8'), contexto, { filename: arquivo });
    return { raiz, document, window, pedidos };
}

test('pix: o botão da linha trava enquanto a cobrança é gerada e volta ao fechar', async () => {
    const cenario = montar('pix', { raizDataset: {} });
    const botao = criarElemento({ pagamentoId: '42' });
    botao.textContent = 'Pagar com Pix';

    cenario.document.emitir('click', { target: { closest: () => botao } });
    assert.ok(ocupado(botao), 'o botão deveria estar travado durante a geração');
    assert.equal(botao.textContent, 'Gerando Pix…');
    assert.equal(cenario.pedidos.length, 1);
    assert.equal(cenario.pedidos[0].opcoes.method, 'POST');

    cenario.pedidos[0].resolve({
        ok: true,
        json: async () => ({ status: 'pendente', valor: 150, pix_copia_cola: 'pix-teste' }),
    });
    await flush();
    // O diálogo já mostra o Pix: o giro para e o rótulo volta, mesmo antes de fechar.
    assert.equal(botao.getAttribute('aria-busy'), null);
    assert.equal(botao.textContent, 'Pagar com Pix');
    assert.equal(botao.disabled, true, 'segue travado enquanto o diálogo modal está aberto');

    cenario.raiz.emitir('cancel');
    assert.ok(livre(botao), 'fechar o diálogo devolve o botão original');
    assert.equal(botao.textContent, 'Pagar com Pix');
});

test('pix: falha na geração também devolve o botão da linha', async () => {
    const cenario = montar('pix', { raizDataset: {} });
    const botao = criarElemento({ pagamentoId: '42' });
    botao.textContent = 'Pagar com Pix';

    cenario.document.emitir('click', { target: { closest: () => botao } });
    assert.ok(ocupado(botao));

    cenario.pedidos[0].reject(new Error('Falha de rede simulada'));
    await flush();
    assert.equal(botao.getAttribute('aria-busy'), null, 'o giro para quando a geração falha');
    assert.equal(botao.textContent, 'Pagar com Pix');

    cenario.raiz.emitir('cancel');
    assert.ok(livre(botao));
    assert.equal(botao.textContent, 'Pagar com Pix');
});

test('pix: clique repetido no mesmo botão não dispara uma segunda cobrança', async () => {
    const cenario = montar('pix', { raizDataset: {} });
    const botao = criarElemento({ pagamentoId: '42' });

    cenario.document.emitir('click', { target: { closest: () => botao } });
    cenario.document.emitir('click', { target: { closest: () => botao } });
    assert.equal(cenario.pedidos.length, 1);
});

for (const [nome, responder] of [
    ['sucesso', (pedido) => pedido.resolve({ ok: true, json: async () => ({ status: 'pendente', pix_copia_cola: 'x' }) })],
    ['erro do servidor', (pedido) => pedido.resolve({ ok: false, json: async () => ({ erro: 'Indisponível' }) })],
    ['falha de rede', (pedido) => pedido.reject(new Error('offline'))],
]) {
    test(`pagamento: "tentar novamente" volta ao normal depois de ${nome}`, async () => {
        const botao = criarElemento();
        botao.textContent = 'Tentar novamente';
        const cenario = montar('pagamento', {
            raizDataset: { pagamentoId: '7', statusInicial: 'cancelado' },
            extras: {
                querySelectorAll(seletor) {
                    return seletor === '[data-tentar-novamente]' ? [botao] : [];
                },
            },
        });

        botao.emitir('click');
        assert.ok(ocupado(botao), 'o botão deveria travar durante a geração');
        assert.equal(botao.textContent, 'Gerando cobrança…');
        assert.equal(cenario.pedidos.length, 1);

        responder(cenario.pedidos[0]);
        await flush();
        await flush();

        assert.ok(livre(botao), 'o botão precisa voltar a ser clicável');
        assert.equal(botao.textContent, 'Tentar novamente');
    });
}
