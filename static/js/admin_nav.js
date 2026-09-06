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
