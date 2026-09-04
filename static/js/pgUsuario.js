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
            botao.disabled = true;
            botao.textContent = 'Plano atual';
        }
    });
}

// ---------- Marca a seção visível no momento como ativa no menu (cabeçalho e navegação inferior) ----------
(() => {
    const idsSecoes = ['turmas', 'mensalidades', 'planos', 'meus-dados'];
    const secoes = idsSecoes.map((id) => document.getElementById(id)).filter(Boolean);
    if (!secoes.length) return;

    const links = Array.from(document.querySelectorAll(
        '.app-header nav a[href^="#"]:not(.nav-avatar-link), .bottom-nav a[href^="#"]'
    ));
    if (!links.length) return;

    let idAtivo = null;

    function marcarAtivo(id) {
        if (id === idAtivo) return;
        idAtivo = id;
        links.forEach((link) => {
            const ativo = link.getAttribute('href') === `#${id}`;
            link.classList.toggle('is-active', ativo);
            if (ativo) {
                link.setAttribute('aria-current', 'page');
            } else {
                link.removeAttribute('aria-current');
            }
        });
    }

    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entradas) => {
            const visiveis = entradas.filter((entrada) => entrada.isIntersecting);
            if (!visiveis.length) return;
            visiveis.sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
            marcarAtivo(visiveis[0].target.id);
        }, { rootMargin: '-35% 0px -55% 0px', threshold: 0 });

        secoes.forEach((secao) => observer.observe(secao));
    } else {
        const aoRolar = () => {
            const referencia = window.scrollY + window.innerHeight * 0.3;
            let atual = secoes[0].id;
            secoes.forEach((secao) => {
                if (secao.offsetTop <= referencia) atual = secao.id;
            });
            marcarAtivo(atual);
        };
        window.addEventListener('scroll', aoRolar, { passive: true });
        aoRolar();
    }

    links.forEach((link) => {
        link.addEventListener('click', () => {
            marcarAtivo(link.getAttribute('href').slice(1));
        });
    });
})();
