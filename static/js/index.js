// Controle do modal de login e comportamentos da página inicial. O modal é um
// <dialog>: foco preso, Esc e fundo inerte vêm do navegador.
const modal = document.getElementById('meuModal');
const input_senha = document.getElementById('senhausuario');
const icone_senha = document.getElementById('iconeSenha');
let ultimoGatilhoModal = null;

function abrirmodal(evento) {
  if (!modal) return;
  ultimoGatilhoModal = evento && evento.currentTarget instanceof HTMLElement
    ? evento.currentTarget
    : document.activeElement;
  if (!modal.open) modal.showModal();
  // O usuário lembrado já veio do auth.js, com a mesma regra da tela de login.
  const inputNome = document.getElementById('inputnome');
  if (inputNome) inputNome.focus();
}

function fechar() {
  if (modal && modal.open) modal.close();
}

// Fechado por Esc, pelo X ou pelo clique fora: o foco volta a quem abriu.
if (modal) {
  modal.addEventListener('close', function () {
    if (ultimoGatilhoModal instanceof HTMLElement) ultimoGatilhoModal.focus();
  });
  modal.addEventListener('click', function (evento) {
    const caixa = modal.getBoundingClientRect();
    const fora = evento.clientX < caixa.left || evento.clientX > caixa.right
      || evento.clientY < caixa.top || evento.clientY > caixa.bottom;
    if (fora) fechar();
  });
}

function mostrarSenha() {
  if (!input_senha || !icone_senha) return;
  if (input_senha.type === 'password') {
    input_senha.type = 'text';
    icone_senha.textContent = 'Ocultar';
    icone_senha.setAttribute('aria-label', 'Ocultar senha');
  } else {
    input_senha.type = 'password';
    icone_senha.textContent = 'Ver';
    icone_senha.setAttribute('aria-label', 'Mostrar senha');
  }
}

document.querySelectorAll('[data-abrir-login]').forEach(function (botao) {
  botao.addEventListener('click', abrirmodal);
});

document.querySelectorAll('[data-fechar-login]').forEach(function (botao) {
  botao.addEventListener('click', fechar);
});

if (icone_senha) {
  icone_senha.addEventListener('click', mostrarSenha);
}

// O cabeçalho rola embora com o hero: fora da tela, a pílula fixa assume o botão dele.
const cabecalho = document.querySelector('.home-header');
const entrarFixo = document.querySelector('[data-entrar-fixo]');
if (cabecalho && entrarFixo && 'IntersectionObserver' in window) {
  new IntersectionObserver(function (entradas) {
    entrarFixo.classList.toggle('is-visivel', !entradas[0].isIntersecting);
  }).observe(cabecalho);
}
