// Controle do modal de login e comportamentos da página inicial
const modal = document.getElementById('meuModal');
const input_senha = document.getElementById('senhausuario');
const icone_senha = document.getElementById('iconeSenha');

function abrirmodal() {
  if (!modal) return;
  modal.hidden = false;
  document.body.classList.add('modal-open');
  const inputNome = document.getElementById('inputnome');
  if (inputNome) {
    // Carrega usuário lembrado, se existir e campo vazio
    try {
      const salvo = localStorage.getItem('et_lembrar_usuario');
      const checkLembrar = document.getElementById('modal_lembrar_usuario');
      if (salvo && !inputNome.value) {
        inputNome.value = salvo;
        if (checkLembrar) checkLembrar.checked = true;
      }
    } catch (e) {}
    inputNome.focus();
  }
}

function fechar() {
  if (!modal) return;
  modal.hidden = true;
  document.body.classList.remove('modal-open');
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

document.addEventListener('keydown', function (evento) {
  if (evento.key === 'Escape' && modal && !modal.hidden) fechar();
});

document.querySelectorAll('[data-abrir-login]').forEach(function (botao) {
  botao.addEventListener('click', abrirmodal);
});

document.querySelectorAll('[data-fechar-login]').forEach(function (botao) {
  botao.addEventListener('click', fechar);
});

if (icone_senha) {
  icone_senha.addEventListener('click', mostrarSenha);
}

// Lembrar usuário no envio do formulário do modal
if (modal) {
  const form = modal.querySelector('form');
  if (form) {
    form.addEventListener('submit', function () {
      try {
        const inputNome = document.getElementById('inputnome');
        const checkLembrar = document.getElementById('modal_lembrar_usuario');
        if (checkLembrar && checkLembrar.checked && inputNome && inputNome.value.trim()) {
          localStorage.setItem('et_lembrar_usuario', inputNome.value.trim());
        } else if (checkLembrar && !checkLembrar.checked) {
          localStorage.removeItem('et_lembrar_usuario');
        }
      } catch (e) {}
    });
  }
}
