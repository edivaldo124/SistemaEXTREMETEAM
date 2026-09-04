(() => {
    const dialog = document.getElementById('pix-dialog');
    if (!dialog) return;

    const estados = {
        carregando: dialog.querySelector('[data-pix-estado="carregando"]'),
        erro: dialog.querySelector('[data-pix-estado="erro"]'),
        pronto: dialog.querySelector('[data-pix-estado="pronto"]'),
    };
    const elErroMsg = dialog.querySelector('[data-pix-erro-msg]');
    const btnTentarNovamente = dialog.querySelector('[data-pix-tentar-novamente]');
    const btnFechar = dialog.querySelector('[data-pix-fechar]');
    const elValor = dialog.querySelector('[data-pix-valor]');
    const elVencimento = dialog.querySelector('[data-pix-vencimento]');
    const elQr = dialog.querySelector('[data-pix-qr]');
    const elSemQr = dialog.querySelector('[data-pix-sem-qr]');
    const elCopiaCola = dialog.querySelector('[data-pix-copia-cola]');
    const btnCopiar = dialog.querySelector('[data-pix-copiar]');
    const elStatus = dialog.querySelector('[data-pix-status]');

    const formatadorPreco = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });
    const formatadorData = new Intl.DateTimeFormat('pt-BR', { timeZone: 'UTC' });

    const MENSAGEM_ERRO_PADRAO = 'Não foi possível gerar o Pix. Tente novamente.';
    const MENSAGENS_HTTP = {
        401: 'Sua sessão expirou. Atualize a página e faça login novamente.',
        403: 'Você não tem permissão para pagar esta mensalidade.',
        404: 'Mensalidade não encontrada.',
        409: 'Esta mensalidade não está mais disponível para pagamento via Pix.',
        422: 'Não foi possível gerar o Pix: verifique se o seu cadastro tem um e-mail válido.',
        502: 'O Mercado Pago recusou a geração da cobrança. Tente novamente.',
        503: 'O Mercado Pago está indisponível no momento. Tente novamente em instantes.',
    };

    let pagamentoIdAtual = null;
    let botaoQueAbriu = null;
    let intervaloPolling = null;

    function mostrarEstado(nome) {
        Object.entries(estados).forEach(([chave, el]) => {
            if (el) el.hidden = chave !== nome;
        });
    }

    async function lerJson(resposta) {
        try {
            return await resposta.json();
        } catch (erro) {
            return null;
        }
    }

    function mensagemDeErro(resposta, dados) {
        return (dados && dados.erro) || MENSAGENS_HTTP[resposta.status] || MENSAGEM_ERRO_PADRAO;
    }

    function pararPolling() {
        if (intervaloPolling) {
            clearInterval(intervaloPolling);
            intervaloPolling = null;
        }
    }

    function limparConteudoAnterior() {
        elValor.textContent = '—';
        elVencimento.textContent = '—';
        elQr.removeAttribute('src');
        elQr.hidden = true;
        elSemQr.hidden = true;
        elCopiaCola.value = '';
        elStatus.textContent = 'Aguardando pagamento…';
        elStatus.classList.remove('pix-status-aprovado');
        elErroMsg.textContent = MENSAGEM_ERRO_PADRAO;
    }

    function fecharDialog() {
        pararPolling();
        pagamentoIdAtual = null;
        if (dialog.open) dialog.close();
        if (botaoQueAbriu) {
            botaoQueAbriu.disabled = false;
            botaoQueAbriu.focus();
        }
        botaoQueAbriu = null;
    }

    function preencherDados(dados) {
        elValor.textContent = formatadorPreco.format(Number(dados.valor));
        elVencimento.textContent = dados.vencimento ? formatadorData.format(new Date(dados.vencimento)) : '—';
        elCopiaCola.value = dados.pix_copia_cola || '';

        if (dados.qr_code_base64) {
            elQr.src = 'data:image/png;base64,' + dados.qr_code_base64;
            elQr.hidden = false;
            elSemQr.hidden = true;
        } else {
            elQr.hidden = true;
            elSemQr.hidden = !dados.pix_copia_cola;
        }

        atualizarStatusTexto(dados.status);
        mostrarEstado('pronto');
    }

    function atualizarStatusTexto(status) {
        if (status === 'pago') {
            elStatus.textContent = 'Pagamento aprovado! Atualizando a página...';
            elStatus.classList.add('pix-status-aprovado');
        } else {
            elStatus.textContent = 'Aguardando pagamento…';
            elStatus.classList.remove('pix-status-aprovado');
        }
    }

    function mostrarExpirado() {
        pararPolling();
        elErroMsg.textContent = 'O código Pix expirou. Gere um novo código para continuar.';
        mostrarEstado('erro');
    }

    function iniciarPolling(pagamentoId) {
        pararPolling();
        intervaloPolling = setInterval(async () => {
            try {
                const resposta = await fetch(`/api/mensalidades/${pagamentoId}/status`, {
                    headers: { Accept: 'application/json' },
                });
                if (!resposta.ok) return;
                const dados = await lerJson(resposta);
                if (!dados) return;

                if (dados.pix_expirado) {
                    mostrarExpirado();
                    return;
                }

                atualizarStatusTexto(dados.status);

                if (dados.status === 'pago') {
                    pararPolling();
                    setTimeout(() => window.location.reload(), 1500);
                }
            } catch (erro) {
                // Falha passageira de rede: mantem o polling, tenta de novo no proximo ciclo.
                console.warn('Falha ao consultar status do Pix.', erro);
            }
        }, 5000);
    }

    async function abrirPix(pagamentoId) {
        pagamentoIdAtual = pagamentoId;
        limparConteudoAnterior();
        mostrarEstado('carregando');
        if (!dialog.open) dialog.showModal();

        try {
            const resposta = await fetch(`/api/mensalidades/${pagamentoId}/pix`, {
                method: 'POST',
                headers: { Accept: 'application/json' },
            });
            const dados = await lerJson(resposta);

            if (!resposta.ok) {
                elErroMsg.textContent = mensagemDeErro(resposta, dados);
                mostrarEstado('erro');
                return;
            }

            if (!dados) {
                elErroMsg.textContent = 'Resposta inesperada do servidor. Tente novamente.';
                mostrarEstado('erro');
                return;
            }

            if (dados.pix_expirado) {
                mostrarExpirado();
                return;
            }

            preencherDados(dados);

            if (dados.status === 'pago') {
                pararPolling();
                setTimeout(() => window.location.reload(), 1500);
            } else {
                iniciarPolling(pagamentoId);
            }
        } catch (erro) {
            elErroMsg.textContent = 'Falha de conexão. Verifique sua internet e tente novamente.';
            mostrarEstado('erro');
        }
    }

    document.addEventListener('click', (event) => {
        const botao = event.target.closest('[data-pix-pagar]');
        if (!botao) return;
        if (dialog.open) return; // ja existe um Pix aberto - ignora clique duplicado
        const pagamentoId = botao.dataset.pagamentoId;
        if (!pagamentoId) return;

        botaoQueAbriu = botao;
        botao.disabled = true;
        abrirPix(pagamentoId);
    });

    btnTentarNovamente?.addEventListener('click', () => {
        if (pagamentoIdAtual) abrirPix(pagamentoIdAtual);
    });

    btnFechar?.addEventListener('click', fecharDialog);
    dialog.addEventListener('cancel', fecharDialog);
    dialog.addEventListener('click', (event) => {
        const box = dialog.getBoundingClientRect();
        const fora = event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom;
        if (fora) fecharDialog();
    });

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
        setTimeout(() => { btnCopiar.textContent = textoOriginal; }, 2000);
    });

    window.addEventListener('pagehide', pararPolling);
})();
