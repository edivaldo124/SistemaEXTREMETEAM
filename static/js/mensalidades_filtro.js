(() => {
    const corpo = document.getElementById('corpo-historico-mensalidades');
    if (!corpo) return;

    const filtroStatus = document.getElementById('filtro-status-mensalidade');
    const filtroCompetencia = document.getElementById('filtro-competencia-mensalidade');
    const botaoLimpar = document.getElementById('limpar-filtros-mensalidade');
    const linhas = Array.from(corpo.querySelectorAll('.linha-mensalidade'));
    const semResultados = document.getElementById('sem-resultados-mensalidade');

    function aplicarFiltros() {
        const status = filtroStatus.value;
        const competencia = filtroCompetencia.value;
        let visiveis = 0;

        linhas.forEach((linha) => {
            const combinaStatus = !status || linha.dataset.status === status;
            const combinaCompetencia = !competencia || linha.dataset.competencia === competencia;
            const deveAparecer = combinaStatus && combinaCompetencia;
            linha.hidden = !deveAparecer;
            if (deveAparecer) visiveis += 1;
        });

        if (semResultados) {
            semResultados.hidden = visiveis !== 0 || linhas.length === 0;
        }
    }

    filtroStatus?.addEventListener('change', aplicarFiltros);
    filtroCompetencia?.addEventListener('change', aplicarFiltros);
    botaoLimpar?.addEventListener('click', () => {
        filtroStatus.value = '';
        filtroCompetencia.value = '';
        aplicarFiltros();
    });
})();
