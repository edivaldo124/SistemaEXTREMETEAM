// Extreme Team - Funcionalidades de autenticação (cliente)
// - Lembrar usuário em localStorage (apenas nome de usuário, nunca senha)
// - Alternar visualização de senha
// - Transição suave entre Login e Cadastro (melhoria progressiva)

document.addEventListener('DOMContentLoaded', function () {
  // 1. Recuperar usuário salvo no aparelho
  try {
    var usuarioSalvo = localStorage.getItem('et_lembrar_usuario');
    if (usuarioSalvo) {
      var inputUser = document.getElementById('loginusuario') || document.getElementById('inputnome');
      var checkLembrar = document.getElementById('lembrar_usuario') || document.getElementById('modal_lembrar_usuario');
      if (inputUser && !inputUser.value) {
        inputUser.value = usuarioSalvo;
      }
      if (checkLembrar) {
        checkLembrar.checked = true;
      }
    }
  } catch (e) {
    // Storage bloqueado em alguns modos privativos
  }

  // 2. Gravar / remover usuário salvo no envio do formulário
  document.addEventListener('submit', function (event) {
    var form = event.target;
    var checkLembrar = form.querySelector('#lembrar_usuario') || form.querySelector('#modal_lembrar_usuario');
    var inputUser = form.querySelector('#loginusuario') || form.querySelector('#inputnome');
    if (checkLembrar && inputUser) {
      try {
        if (checkLembrar.checked && inputUser.value.trim()) {
          localStorage.setItem('et_lembrar_usuario', inputUser.value.trim());
        } else {
          localStorage.removeItem('et_lembrar_usuario');
        }
      } catch (e) {
        // Storage bloqueado
      }
    }
  });

  // 3. Mostrar / ocultar senha
  document.querySelectorAll('.password-toggle').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var wrap = btn.closest('.input-wrap, .campo-senha, .field');
      if (!wrap) return;
      var input = wrap.querySelector('input[name*="senha"], input[id*="senha"]');
      if (!input) return;
      var showing = input.type === 'text';
      input.type = showing ? 'password' : 'text';
      btn.setAttribute('aria-pressed', String(!showing));
      btn.setAttribute('aria-label', showing ? 'Mostrar senha' : 'Ocultar senha');
    });
  });

  // 4. Transição de rota Login ⇄ Cadastro (melhoria progressiva)
  document.querySelectorAll('[data-auth-swap]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        return; // Transição desligada sob preferência de movimento reduzido
      }
      if (document.startViewTransition) {
        // Se a API nativa de View Transitions for suportada, o navegador cuida da transição
        return;
      }
      e.preventDefault();
      var destino = link.getAttribute('href');
      var shell = document.querySelector('.auth-shell, .login-shell, .register-shell');
      if (shell) {
        shell.classList.add('auth-transitioning');
        setTimeout(function () {
          window.location.href = destino;
        }, 200);
      } else {
        window.location.href = destino;
      }
    });
  });
});
