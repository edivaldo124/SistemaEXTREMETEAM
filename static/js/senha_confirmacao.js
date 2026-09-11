// Confirmação de senha no navegador. A mesma comparação é refeita no servidor: isto
// aqui só antecipa o aviso para a pessoa não perder o formulário preenchido.
// O valor digitado não sai do campo - nada é guardado nem enviado a outro lugar.
document.querySelectorAll('[data-confirmar-senha]').forEach(function (confirmacao) {
  var senha = document.getElementById(confirmacao.dataset.confirmarSenha);
  if (!senha) return;

  var aviso = document.getElementById(confirmacao.getAttribute('aria-describedby'));
  var mensagem = (aviso && aviso.textContent.trim()) || 'As duas senhas precisam ser iguais.';

  function verificar() {
    var divergente = confirmacao.value !== '' && confirmacao.value !== senha.value;
    confirmacao.setCustomValidity(divergente ? mensagem : '');
    confirmacao.setAttribute('aria-invalid', divergente ? 'true' : 'false');
    if (aviso) aviso.hidden = !divergente;
  }

  senha.addEventListener('input', verificar);
  confirmacao.addEventListener('input', verificar);
  confirmacao.addEventListener('blur', verificar);
});
