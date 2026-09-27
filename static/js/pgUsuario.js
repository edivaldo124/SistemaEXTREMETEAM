// ---------- Navegação da área do aluno: uma tela por item do menu ----------
(() => {
    const idsTelas = ['visao-geral', 'turmas', 'mensalidades', 'planos', 'meus-dados'];
    const telas = idsTelas.map((id) => document.getElementById(id)).filter(Boolean);
    const links = Array.from(document.querySelectorAll('[data-menu-screen]'));
    if (!telas.length || !links.length) return;

    let telaAtual = null;

    function mostrarTela(id, moverFoco = false) {
        if (!idsTelas.includes(id)) id = 'visao-geral';
        telaAtual = id;
        telas.forEach((tela) => {
            const ativa = tela.id === id;
            tela.hidden = !ativa;
            tela.setAttribute('aria-hidden', String(!ativa));
        });
        links.forEach((link) => {
            const ativo = link.dataset.menuScreen === id;
            link.classList.toggle('is-active', ativo);
            if (ativo) link.setAttribute('aria-current', 'page');
            else link.removeAttribute('aria-current');
        });
        if (moverFoco) document.getElementById(id)?.focus({ preventScroll: true });
        window.scrollTo({ top: 0, behavior: 'auto' });
    }

    links.forEach((link) => {
        link.addEventListener('click', (evento) => {
            evento.preventDefault();
            const id = link.dataset.menuScreen;
            history.pushState(null, '', `#${id}`);
            trocarTela(id, true);
        });
    });

    // A tela nova entra pelo lado em que está no menu. deslizarTela vem de
    // components/deslize.html; sem ele a troca é seca, como antes.
    function trocarTela(id, moverFoco = false) {
        if (!idsTelas.includes(id)) id = 'visao-geral';
        if (id === telaAtual) return;
        const sentido = idsTelas.indexOf(id) > idsTelas.indexOf(telaAtual) ? 'avanca' : 'volta';
        // popstate e hashchange chegam juntos no "voltar"; a tela conta como
        // trocada já aqui, antes da transição rodar a atualização.
        telaAtual = id;
        document.body.classList.add('telas-trocadas');
        const atualizar = () => mostrarTela(id, moverFoco);
        if (window.deslizarTela) window.deslizarTela(sentido, atualizar);
        else atualizar();
    }

    window.addEventListener('popstate', () => trocarTela(location.hash.slice(1)));
    window.addEventListener('hashchange', () => trocarTela(location.hash.slice(1)));
    mostrarTela(location.hash.slice(1) || 'visao-geral');
})();
