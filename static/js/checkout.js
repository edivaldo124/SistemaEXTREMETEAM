// Checkout Pro ("outras formas de pagamento"): abre a preferência criada pelo servidor
// e, na tela de retorno, reconsulta o backend até haver um estado
// confirmado. Nada aqui decide se o pagamento foi aprovado - quem decide é o servidor,
// que só confia na API do Mercado Pago.
(() => {
    // ---------------------------------------------------------- abertura do checkout --
    // O POST termina no nosso servidor. A navegação externa é um GET separado,
    // permitido mesmo quando a política de segurança restringe form-action a self.
    const LIMITE_ABERTURA_MS = 15000;
    const HOSTS_CHECKOUT = new Set(['www.mercadopago.com.br', 'sandbox.mercadopago.com.br']);
    const formularios = new Map();
    const aberturas = new Map();

    function prepararFormulario(form) {
        if (formularios.has(form)) return formularios.get(form);
        const botao = form.querySelector('[data-checkout-abrir]');
        if (!botao) return null;
        const mensagem = document.createElement('p');
        mensagem.className = 'alert';
        mensagem.setAttribute('role', 'alert');
        mensagem.setAttribute('data-checkout-erro', '');
        mensagem.hidden = true;
        form.append(mensagem);
        const estado = { botao, mensagem, conteudoOriginal: Array.from(botao.childNodes) };
        formularios.set(form, estado);
        return estado;
    }

    function finalizarAbertura(form, abertura, erro = '') {
        if (aberturas.get(form) !== abertura) return;
        clearTimeout(abertura.timer);
        aberturas.delete(form);
        const estado = formularios.get(form);
        estado.botao.disabled = false;
        estado.botao.replaceChildren(...estado.conteudoOriginal);
        form.removeAttribute('aria-busy');
        estado.mensagem.textContent = erro;
        estado.mensagem.hidden = !erro;
    }

    function cancelarAberturas() {
        for (const [form, abertura] of aberturas) {
            finalizarAbertura(form, abertura);
            abertura.controlador.abort();
        }
    }

    document.querySelectorAll('.form-outras-formas').forEach(prepararFormulario);

    document.addEventListener('submit', async (event) => {
        const form = event.target.closest('.form-outras-formas');
        if (!form) return;
        const estado = prepararFormulario(form);
        if (!estado) return;
        event.preventDefault();
        if (aberturas.has(form)) return;

        const abertura = { controlador: new AbortController(), timer: null };
        aberturas.set(form, abertura);
        estado.botao.disabled = true;
        estado.botao.textContent = 'Abrindo checkout…';
        estado.mensagem.hidden = true;
        estado.mensagem.textContent = '';
        form.setAttribute('aria-busy', 'true');
        abertura.timer = setTimeout(() => {
            finalizarAbertura(form, abertura, 'O pagamento demorou para responder. Tente novamente em instantes.');
            abertura.controlador.abort();
        }, LIMITE_ABERTURA_MS);

        try {
            const destino = new URL(form.action, window.location.href);
            if (destino.origin !== window.location.origin) throw new Error('Destino de pagamento inválido. Recarregue a página.');
            const resposta = await fetch(destino.href, {
                method: 'POST',
                credentials: 'same-origin',
                mode: 'same-origin',
                redirect: 'error',
                headers: { Accept: 'application/json' },
                body: new FormData(form),
                signal: abertura.controlador.signal,
            });
            if (aberturas.get(form) !== abertura) return;
            if (resposta.status === 401) throw new Error('Sua sessão expirou. Recarregue a página e entre novamente.');
            const tipo = resposta.headers.get('content-type') || '';
            if (!tipo.includes('application/json')) {
                if (resposta.status === 400) throw new Error('Não foi possível validar o formulário. Recarregue a página e tente novamente.');
                throw new Error('Não foi possível abrir o pagamento. Recarregue a página e tente novamente.');
            }
            const dados = await resposta.json();
            if (aberturas.get(form) !== abertura) return;
            if (!resposta.ok) {
                throw new Error(typeof dados?.erro === 'string' ? dados.erro : 'Não foi possível abrir o pagamento. Tente novamente.');
            }
            const url = typeof dados?.url_checkout === 'string' ? new URL(dados.url_checkout) : null;
            if (!url || url.protocol !== 'https:' || !HOSTS_CHECKOUT.has(url.hostname) || url.port || url.username || url.password) {
                throw new Error('O endereço do pagamento é inválido. Tente novamente em instantes.');
            }
            window.location.assign(url.href);
            finalizarAbertura(form, abertura);
        } catch (erro) {
            const mensagem = erro instanceof TypeError || erro instanceof SyntaxError
                ? 'Não foi possível conectar ao pagamento. Tente novamente em instantes.'
                : erro.message || 'Não foi possível abrir o pagamento. Tente novamente.';
            finalizarAbertura(form, abertura, mensagem);
        }
    });

    // Cancelar ao sair também impede que uma resposta tardia navegue após voltar.
    window.addEventListener('pagehide', cancelarAberturas);
    window.addEventListener('pageshow', cancelarAberturas);

    // -------------------------------------------------------------- tela de retorno --
    const raiz = document.getElementById('retorno-checkout');
    if (!raiz) return;

    const pagamentoId = raiz.dataset.pagamentoId;
    const statusInicial = raiz.dataset.status;
    const badge = raiz.querySelector('[data-status-badge]');

    // Estados finais: já não muda mais sozinho, não faz sentido continuar consultando.
    const ESTADOS_FINAIS = ['pago', 'cancelado', 'reembolsado', 'recusado', 'em_analise'];
    const INTERVALO_MS = 5000;
    const MAXIMO_CONSULTAS = 24; // ~2 min; depois disso o webhook resolve sem a página aberta

    if (ESTADOS_FINAIS.includes(statusInicial)) return;

    let consultas = 0;
    let intervalo = null;
    let consultaEmAndamento = false;
    let paginaAtiva = true;
    let encerrado = false;

    function parar() {
        if (intervalo) {
            clearInterval(intervalo);
            intervalo = null;
        }
    }

    async function consultar() {
        // Uma consulta lenta não pode ocupar mais conexões a cada cinco segundos.
        if (consultaEmAndamento || !paginaAtiva || encerrado) return;
        consultas += 1;
        if (consultas > MAXIMO_CONSULTAS) {
            encerrado = true;
            parar();
            return;
        }
        consultaEmAndamento = true;
        try {
            const resposta = await fetch(`/api/mensalidades/${pagamentoId}/status`, {
                headers: { Accept: 'application/json' },
            });
            if (!resposta.ok) return;
            const dados = await resposta.json();
            if (!paginaAtiva || encerrado) return;
            if (!dados || !dados.status) return;

            if (badge && dados.status_rotulo) {
                badge.textContent = dados.status_rotulo;
                badge.className = `status status-${dados.status}`;
            }

            // O texto explicativo é montado no servidor: em vez de reescrevê-lo aqui
            // (e arriscar anunciar "aprovado" sem confirmação), recarrega a página.
            if (dados.status !== statusInicial) {
                encerrado = true;
                parar();
                window.location.reload();
            }
        } catch (erro) {
            // Falha passageira de rede: mantém o estado atual e tenta no próximo ciclo.
        } finally {
            consultaEmAndamento = false;
        }
    }

    intervalo = setInterval(consultar, INTERVALO_MS);
    window.addEventListener('pagehide', () => {
        paginaAtiva = false;
        parar();
    });
    window.addEventListener('pageshow', (event) => {
        if (!event.persisted) return;
        paginaAtiva = true;
        if (!encerrado && !intervalo) intervalo = setInterval(consultar, INTERVALO_MS);
    });
})();
