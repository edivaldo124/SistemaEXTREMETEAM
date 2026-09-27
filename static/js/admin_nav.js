// Navegação da administração no celular: diz de que lado ainda há seção fora
// da tela. É estado de rolagem, então precisa de JS; sem ele a fila continua
// rolável, apenas sem o degradê de aviso.
(() => {
    const fila = document.querySelector('.admin-nav-scroll');
    if (!fila) return;

    function marcar() {
        const sobra = fila.scrollWidth - fila.clientWidth;
        if (sobra <= 2) {
            fila.removeAttribute('data-rolagem');
            return;
        }
        const inicio = fila.scrollLeft <= 2;
        const fim = fila.scrollLeft >= sobra - 2;
        fila.dataset.rolagem = inicio ? 'inicio' : (fim ? 'fim' : 'meio');
    }

    // Chegar num item pelo teclado precisa trazê-lo para dentro da área visível.
    fila.addEventListener('focusin', (evento) => {
        const item = evento.target.closest('a');
        if (item) item.scrollIntoView({ block: 'nearest', inline: 'nearest' });
    });

    fila.addEventListener('scroll', marcar, { passive: true });
    window.addEventListener('resize', marcar);
    // A seção ativa começa visível mesmo quando é a última da fila.
    const ativo = fila.querySelector('[aria-current="page"]');
    if (ativo) ativo.scrollIntoView({ block: 'nearest', inline: 'nearest' });
    marcar();
})();

// Abas das telas da administração que recarregam depois de um envio (salvar,
// lançar mensalidade, voltar de uma conexão OAuth): o servidor redireciona para a
// mesma URL sem dizer a aba, então a última aba aberta fica guardada por página
// em sessionStorage. Um #id de aba ou painel na URL tem prioridade. A troca em
// si é de componentes.js; aqui só se escolhe qual aba clicar ao abrir a página.
(() => {
    document.querySelectorAll('[data-tabs][data-tabs-lembrar]').forEach((grupo) => {
        const chave = `et-aba:${location.pathname}:${grupo.dataset.tabsLembrar}`;
        const abas = Array.from(grupo.querySelectorAll('[role="tab"]'));
        const porAlvo = (id) => abas.find((aba) => aba.id === id || aba.getAttribute('aria-controls') === id);

        let guardada = null;
        try { guardada = sessionStorage.getItem(chave); } catch (erro) { /* armazenamento bloqueado */ }
        const inicial = porAlvo(decodeURIComponent(location.hash.slice(1))) || porAlvo(guardada);
        if (inicial && inicial.getAttribute('aria-selected') !== 'true') inicial.click();

        abas.forEach((aba) => aba.addEventListener('click', () => {
            try { sessionStorage.setItem(chave, aba.id); } catch (erro) { /* segue sem lembrar */ }
        }));
    });
})();
