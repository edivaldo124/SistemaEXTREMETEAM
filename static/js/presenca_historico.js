(() => {
    const dialog = document.getElementById('presenca-dialog');
    if (!dialog) return;

    const botaoAbrir = document.querySelector('[data-abrir-presencas]');
    const btnFechar = dialog.querySelector('[data-presenca-fechar]');
    let elementoAnterior = null;

    function abrir() {
        elementoAnterior = document.activeElement;
        dialog.showModal();
    }

    function fechar() {
        if (dialog.open) dialog.close();
        if (elementoAnterior) elementoAnterior.focus();
    }

    botaoAbrir?.addEventListener('click', abrir);
    btnFechar?.addEventListener('click', fechar);
    dialog.addEventListener('cancel', fechar);
    dialog.addEventListener('click', (evento) => {
        const area = dialog.getBoundingClientRect();
        const fora = evento.clientX < area.left || evento.clientX > area.right
            || evento.clientY < area.top || evento.clientY > area.bottom;
        if (fora) fechar();
    });

    const corpo = document.getElementById('corpo-historico-presenca');
    if (!corpo) return;

    const filtroTurma = document.getElementById('filtro-turma-presenca');
    const filtroStatus = document.getElementById('filtro-status-presenca');
    const botaoLimpar = document.getElementById('limpar-filtros-presenca');
    const linhas = Array.from(corpo.querySelectorAll('.linha-presenca'));
    const semResultados = document.getElementById('sem-resultados-presenca');

    function aplicarFiltros() {
        const turma = filtroTurma.value;
        const status = filtroStatus.value;
        let visiveis = 0;

        linhas.forEach((linha) => {
            const combinaTurma = !turma || linha.dataset.turma === turma;
            const combinaStatus = !status || linha.dataset.presente === status;
            const deveAparecer = combinaTurma && combinaStatus;
            linha.hidden = !deveAparecer;
            if (deveAparecer) visiveis += 1;
        });

        if (semResultados) {
            semResultados.hidden = visiveis !== 0 || linhas.length === 0;
        }
    }

    filtroTurma?.addEventListener('change', aplicarFiltros);
    filtroStatus?.addEventListener('change', aplicarFiltros);
    botaoLimpar?.addEventListener('click', () => {
        filtroTurma.value = '';
        filtroStatus.value = '';
        aplicarFiltros();
    });
})();
