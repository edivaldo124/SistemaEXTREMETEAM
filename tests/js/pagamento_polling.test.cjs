const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const flush = () => new Promise((resolve) => setImmediate(resolve));

// Executa os scripts reais com respostas controladas: nenhum pedido sai para a rede.
function criarPagina(script) {
    function elemento(dataset = {}) {
        const eventos = new Map();
        const filhos = new Map();
        const atributos = new Map();
        return {
            dataset, textContent: '', value: '', hidden: false, open: false, atributos,
            classList: { add() {}, remove() {} },
            addEventListener(nome, callback) {
                if (!eventos.has(nome)) eventos.set(nome, []);
                eventos.get(nome).push(callback);
            },
            emitir(nome, evento = {}) {
                for (const callback of eventos.get(nome) || []) callback(evento);
            },
            querySelector(seletor) {
                if (!filhos.has(seletor)) filhos.set(seletor, elemento());
                return filhos.get(seletor);
            },
            querySelectorAll() { return []; },
            showModal() { this.open = true; },
            close() { this.open = false; },
            setAttribute(nome, valor) { atributos.set(nome, String(valor)); },
            getAttribute(nome) { return atributos.has(nome) ? atributos.get(nome) : null; },
            removeAttribute(nome) { atributos.delete(nome); }, focus() {},
        };
    }

    const raiz = elemento({ pagamentoId: '42', statusInicial: 'pendente', status: 'pendente' });
    const document = elemento();
    const window = elemento();
    let recargas = 0;
    window.location = { reload() { recargas += 1; } };
    const idRaiz = { checkout: 'retorno-checkout', pagamento: 'pagina-pagamento', pix: 'pix-dialog' }[script];
    document.getElementById = (id) => id === idRaiz ? raiz : null;

    const intervalos = new Map();
    let proximoTimer = 0;
    const consultas = [];
    const pendente = { status: 'pendente', valor: 10, pix_copia_cola: 'pix-test' };
    const contexto = {
        document, window, Intl, console: { ...console, warn() {} },
        setInterval(callback) {
            const id = ++proximoTimer;
            intervalos.set(id, callback);
            return id;
        },
        clearInterval(id) { intervalos.delete(id); },
        setTimeout() { return ++proximoTimer; },
        fetch(url, opcoes) {
            if (opcoes?.method === 'POST') {
                return Promise.resolve({ ok: true, json: async () => pendente });
            }
            assert.match(url, /^\/api\/mensalidades\/42\/status$/);
            return new Promise((resolve, reject) => consultas.push({ resolve, reject }));
        },
    };
    const arquivo = path.resolve(__dirname, '../../static/js', `${script}.js`);
    vm.runInNewContext(fs.readFileSync(arquivo, 'utf8'), contexto, { filename: arquivo });
    let botaoPix = null;
    if (script === 'pix') {
        botaoPix = elemento({ pagamentoId: '42' });
        document.emitir('click', { target: { closest: () => botaoPix } });
    }

    return {
        consultas, intervalos, raiz, window, botaoPix,
        get recargas() { return recargas; },
        async tick() {
            for (const callback of [...intervalos.values()]) callback();
            await flush();
        },
        async responder(indice, dados = pendente, ok = true) {
            consultas[indice].resolve({ ok, json: async () => dados });
            await flush();
        },
    };
}

for (const script of ['checkout', 'pagamento', 'pix']) {
    test(`${script}: não empilha consultas lentas e retoma depois da resposta`, async () => {
        const pagina = criarPagina(script);
        await flush();
        await pagina.tick();
        await pagina.tick();
        await pagina.tick();
        assert.equal(pagina.consultas.length, 1);

        await pagina.responder(0);
        await pagina.tick();
        assert.equal(pagina.consultas.length, 2);

        pagina.consultas[1].reject(new Error('Falha de rede simulada'));
        await flush();
        await pagina.tick();
        assert.equal(pagina.consultas.length, 3);
    });

    test(`${script}: suspende ao sair e retoma no bfcache sem duplicar pedido pendente`, async () => {
        const pagina = criarPagina(script);
        await flush();
        await pagina.tick();
        pagina.window.emitir('pagehide');
        assert.equal(pagina.intervalos.size, 0);
        await pagina.tick();
        assert.equal(pagina.consultas.length, 1);

        pagina.window.emitir('pageshow', { persisted: true });
        assert.equal(pagina.intervalos.size, 1);
        await pagina.tick();
        assert.equal(pagina.consultas.length, 1);
        await pagina.responder(0);
        await pagina.tick();
        assert.equal(pagina.consultas.length, 2);
    });

    for (const status of ['pago', 'cancelado', 'reembolsado', 'recusado', 'em_analise']) {
        test(`${script}: encerra consultas em ${status}, inclusive após voltar pelo histórico`, async () => {
            const pagina = criarPagina(script);
            await flush();
            await pagina.tick();
            await pagina.responder(0, { status });
            assert.equal(pagina.intervalos.size, 0);
            pagina.window.emitir('pagehide');
            pagina.window.emitir('pageshow', { persisted: true });
            await pagina.tick();
            assert.equal(pagina.consultas.length, 1);
        });
    }
}

test('pix: fechar o diálogo ignora a resposta pendente e impede novas consultas', async () => {
    const pagina = criarPagina('pix');
    await flush();
    await pagina.tick();
    pagina.raiz.emitir('cancel');
    await pagina.responder(0);
    pagina.window.emitir('pagehide');
    pagina.window.emitir('pageshow', { persisted: true });
    await pagina.tick();
    assert.equal(pagina.intervalos.size, 0);
    assert.equal(pagina.consultas.length, 1);
});
