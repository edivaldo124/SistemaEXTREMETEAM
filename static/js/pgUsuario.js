const gradePlanos = document.querySelector('.grid-planos');

const formatadorDePreco = new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
});

document.querySelectorAll('[data-preco]').forEach(function (preco) {
    const valor = Number(preco.dataset.preco);

    if (!Number.isNaN(valor)) {
        preco.textContent = formatadorDePreco.format(valor);
    }
});

if (gradePlanos) {
    const planoAtual = gradePlanos.dataset.planoAtual;

    document.querySelectorAll('.card-plano').forEach(function (card) {
        if (planoAtual && card.dataset.planoId === planoAtual) {
            const botao = card.querySelector('.btn-escolher');
            card.classList.add('plano-atual');
            // O aluno pode estar associado ao plano sem possuir uma mensalidade
            // aberta (cadastros antigos, por exemplo). Manter a ação disponível
            // permite criar ou reutilizar a cobrança com segurança no backend.
            botao.textContent = 'Pagar plano atual';
        }
    });
}

// ---------- Navegação da área do aluno: uma tela por item do menu ----------
(() => {
    const idsTelas = ['visao-geral', 'turmas', 'mensalidades', 'planos', 'meus-dados'];
    const telas = idsTelas.map((id) => document.getElementById(id)).filter(Boolean);
    const links = Array.from(document.querySelectorAll('[data-menu-screen]'));
    if (!telas.length || !links.length) return;

    function mostrarTela(id, moverFoco = false) {
        if (!idsTelas.includes(id)) id = 'visao-geral';
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
            mostrarTela(id, true);
        });
    });

    window.addEventListener('popstate', () => mostrarTela(location.hash.slice(1)));
    window.addEventListener('hashchange', () => mostrarTela(location.hash.slice(1)));
    mostrarTela(location.hash.slice(1) || 'visao-geral');
})();
