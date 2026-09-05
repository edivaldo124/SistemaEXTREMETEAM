(() => {
    const raiz = document.getElementById('pagina-pagamento');
    if (!raiz) return;

    const pagamentoId = raiz.dataset.pagamentoId;
    let statusAtual = raiz.dataset.statusInicial;
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content || '';

    const estados = {};
    raiz.querySelectorAll('[data-estado]').forEach((el) => {
        estados[el.dataset.estado] = el;
    });

    const elErroMsg = raiz.querySelector('[data-erro-msg]');
    const elQr = raiz.querySelector('[data-qr]');
    const elSemQr = raiz.querySelector('[data-sem-qr]');
    const elCopiaCola = raiz.querySelector('[data-copia-cola]');
    const btnCopiar = raiz.querySelector('[data-copiar]');
    const elFalhaCopiar = raiz.querySelector('[data-falha-copiar]');
    const elExpiracao = raiz.querySelector('[data-expiracao]');
    const botoesTentarNovamente = raiz.querySelectorAll('[data-tentar-novamente]');

    const formatadorData = new Intl.DateTimeFormat('pt-BR', { dateStyle: 'short', timeStyle: 'short' });

    let intervaloPolling = null;

    function mostrarEstado(nome) {
        Object.entries(estados).forEach(([chave, el]) => {
            el.hidden = chave !== nome;
        });
    }

    function pararPolling() {
        if (intervaloPolling) {
            clearInterval(intervaloPolling);
            intervaloPolling = null;
        }
    }

    function iniciarPolling() {
        if (intervaloPolling) return;
        intervaloPolling = setInterval(consultarStatus, 5000);
    }

    function tratarResposta(dados) {
        statusAtual = dados.status;

        if (dados.status === 'pago') {
            pararPolling();
            mostrarEstado('aprovado');
            setTimeout(() => {
                window.location.href = `/perfil/mensalidade/${pagamentoId}/comprovante`;
            }, 1200);
            return;
        }
        if (dados.status === 'em_analise') {
            pararPolling();
            mostrarEstado('analise');
            return;
        }
        if (dados.status === 'recusado') {
            pararPolling();
            mostrarEstado('recusado');
            return;
        }
        if (dados.status === 'em_processamento') {
            mostrarEstado('processando');
            iniciarPolling();
            return;
        }
        if (dados.pix_expirado) {
            pararPolling();
            mostrarEstado('expirado');
            return;
        }

        if (elCopiaCola) elCopiaCola.value = dados.pix_copia_cola || '';
        if (dados.qr_code_base64 && elQr) {
            elQr.src = 'data:image/png;base64,' + dados.qr_code_base64;
            elQr.hidden = false;
            if (elSemQr) elSemQr.hidden = true;
        } else if (elSemQr) {
            elSemQr.hidden = !dados.pix_copia_cola;
        }
        if (elExpiracao && dados.data_expiracao) {
            elExpiracao.textContent = formatadorData.format(new Date(dados.data_expiracao));
        }
        mostrarEstado('pix');
        iniciarPolling();
    }

    async function consultarStatus() {
        try {
            const resposta = await fetch(`/api/mensalidades/${pagamentoId}/status`, { headers: { Accept: 'application/json' } });
            if (!resposta.ok) return;
            tratarResposta(await resposta.json());
        } catch (erro) {
            // Falha passageira de rede - mantem o estado atual, tenta de novo no proximo ciclo.
        }
    }

    async function gerarOuAtualizarPix() {
        pararPolling();
        mostrarEstado('carregando');
        try {
            const resposta = await fetch(`/api/mensalidades/${pagamentoId}/pix`, {
                method: 'POST',
                headers: { Accept: 'application/json', 'X-CSRFToken': csrfToken },
            });
            const dados = await resposta.json();

            if (!resposta.ok) {
                if (elErroMsg) elErroMsg.textContent = dados.erro || 'Não foi possível carregar o pagamento. Tente novamente.';
                mostrarEstado('erro');
                return;
            }
            tratarResposta(dados);
        } catch (erro) {
            if (elErroMsg) elErroMsg.textContent = 'Falha de conexão. Verifique sua internet e tente novamente.';
            mostrarEstado('erro');
        }
    }

    btnCopiar?.addEventListener('click', async () => {
        const texto = elCopiaCola.value;
        if (!texto) return;

        let copiado = false;
        try {
            await navigator.clipboard.writeText(texto);
            copiado = true;
        } catch (erro) {
            elCopiaCola.select();
            copiado = document.execCommand && document.execCommand('copy');
        }

        const textoOriginal = btnCopiar.textContent;
        btnCopiar.textContent = copiado ? 'Copiado!' : 'Não foi possível copiar';
        if (elFalhaCopiar) elFalhaCopiar.hidden = copiado;
        setTimeout(() => { btnCopiar.textContent = textoOriginal; }, 2000);
    });

    botoesTentarNovamente.forEach((botao) => botao.addEventListener('click', gerarOuAtualizarPix));

    if (['pendente', 'atrasado', 'recusado'].includes(statusAtual)) {
        gerarOuAtualizarPix();
    } else if (statusAtual === 'em_processamento') {
        mostrarEstado('processando');
        iniciarPolling();
    } else if (statusAtual === 'em_analise') {
        mostrarEstado('analise');
    } else if (statusAtual === 'pago') {
        mostrarEstado('aprovado');
    } else {
        mostrarEstado('encerrado');
    }
})();
