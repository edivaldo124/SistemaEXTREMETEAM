// Financeiro no celular: a faixa de filtros ocupa quase uma tela inteira antes
// da primeira mensalidade. Aqui ela vira um bloco recolhível — o resumo dos
// filtros aplicados continua sempre visível, então nada some sem aviso.
// Sem JS o botão fica oculto e o formulário permanece aberto.
(() => {
    const botao = document.querySelector('[data-filtros-alternar]');
    const formulario = document.getElementById('filtros-financeiro');
    if (!botao || !formulario) return;

    const texto = botao.querySelector('[data-filtros-alternar-texto]');
    const estreito = window.matchMedia('(max-width: 900px)');
    let escolhaDoUsuario = null;

    function aplicar(aberto) {
        formulario.hidden = !aberto;
        botao.setAttribute('aria-expanded', String(aberto));
        if (texto) texto.textContent = aberto ? 'Ocultar filtros' : 'Mostrar filtros';
    }

    function ajustar() {
        botao.hidden = !estreito.matches;
        if (!estreito.matches) {
            aplicar(true);
            return;
        }
        // No celular começa fechado, a não ser que a pessoa já tenha aberto.
        aplicar(escolhaDoUsuario === null ? false : escolhaDoUsuario);
    }

    botao.addEventListener('click', () => {
        escolhaDoUsuario = formulario.hidden;
        aplicar(escolhaDoUsuario);
        if (escolhaDoUsuario) formulario.querySelector('input, select')?.focus();
    });

    estreito.addEventListener('change', ajustar);
    ajustar();
})();
