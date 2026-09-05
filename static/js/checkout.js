// Checkout Pro ("outras formas de pagamento"): protege contra clique duplo no botão que
// cria a preferência e, na tela de retorno, reconsulta o backend até haver um estado
// confirmado. Nada aqui decide se o pagamento foi aprovado - quem decide é o servidor,
// que só confia na API do Mercado Pago.
(() => {
    // ---------------------------------------------------------------- clique duplo --
    // Cada envio cria/reutiliza uma preferência no servidor; travar o botão evita
    // disparar duas navegações enquanto o redirecionamento não acontece.
    document.addEventListener('submit', (event) => {
        const form = event.target.closest('.form-outras-formas');
        if (!form) return;
        const botao = form.querySelector('[data-checkout-abrir]');
        if (!botao) return;
        if (botao.disabled) {
            event.preventDefault();
            return;
        }
        botao.disabled = true;
        botao.dataset.textoOriginal = botao.textContent;
        botao.textContent = 'Abrindo checkout…';
    });

    // Voltar pelo histórico (inclusive bfcache) precisa devolver o botão utilizável.
    window.addEventListener('pageshow', () => {
        document.querySelectorAll('[data-checkout-abrir][disabled]').forEach((botao) => {
            botao.disabled = false;
            if (botao.dataset.textoOriginal) botao.textContent = botao.dataset.textoOriginal;
        });
    });

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

    function parar() {
        if (intervalo) {
            clearInterval(intervalo);
            intervalo = null;
        }
    }

    async function consultar() {
        consultas += 1;
        if (consultas > MAXIMO_CONSULTAS) {
            parar();
            return;
        }
        try {
            const resposta = await fetch(`/api/mensalidades/${pagamentoId}/status`, {
                headers: { Accept: 'application/json' },
            });
            if (!resposta.ok) return;
            const dados = await resposta.json();
            if (!dados || !dados.status) return;

            if (badge && dados.status_rotulo) {
                badge.textContent = dados.status_rotulo;
                badge.className = `status status-${dados.status}`;
            }

            // O texto explicativo é montado no servidor: em vez de reescrevê-lo aqui
            // (e arriscar anunciar "aprovado" sem confirmação), recarrega a página.
            if (dados.status !== statusInicial) {
                parar();
                window.location.reload();
            }
        } catch (erro) {
            // Falha passageira de rede: mantém o estado atual e tenta no próximo ciclo.
        }
    }

    intervalo = setInterval(consultar, INTERVALO_MS);
    window.addEventListener('pagehide', parar);
})();
