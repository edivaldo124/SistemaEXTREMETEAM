(() => {
    const dialog = document.getElementById('comprovante-dialog');
    if (!dialog) return;

    const elAluno = dialog.querySelector('[data-comprovante-aluno]');
    const elValor = dialog.querySelector('[data-comprovante-valor]');
    const elCompetencia = dialog.querySelector('[data-comprovante-competencia]');
    const elEnviado = dialog.querySelector('[data-comprovante-enviado]');
    const elImg = dialog.querySelector('[data-comprovante-img]');
    const elSemPreview = dialog.querySelector('[data-comprovante-sem-preview]');
    const elAbrir = dialog.querySelector('[data-comprovante-abrir]');
    const formAprovar = dialog.querySelector('[data-comprovante-form-aprovar]');
    const formRejeitar = dialog.querySelector('[data-comprovante-form-rejeitar]');
    const btnFechar = dialog.querySelector('[data-comprovante-fechar]');

    let elementoAnterior = null;

    function abrirDialog(botao) {
        elementoAnterior = document.activeElement;

        elAluno.textContent = botao.dataset.alunoNome || '—';
        // Já chega formatado do servidor (filtro `moeda`), com o R$ incluído.
        elValor.textContent = botao.dataset.valor || '—';
        elCompetencia.textContent = botao.dataset.competencia || '—';
        elEnviado.textContent = botao.dataset.enviadoEm || '—';

        const urlArquivo = botao.dataset.arquivoUrl || '';
        elAbrir.href = urlArquivo;

        elImg.hidden = true;
        elSemPreview.hidden = true;
        elImg.onload = () => { elImg.hidden = false; };
        elImg.onerror = () => { elImg.hidden = true; elSemPreview.hidden = false; };
        elImg.src = urlArquivo;

        formAprovar.action = botao.dataset.aprovarAction || '';
        formRejeitar.action = botao.dataset.rejeitarAction || '';

        dialog.showModal();
    }

    function fecharDialog() {
        if (dialog.open) dialog.close();
        elImg.removeAttribute('src');
        if (elementoAnterior) elementoAnterior.focus();
    }

    document.addEventListener('click', (evento) => {
        const botao = evento.target.closest('[data-abrir-comprovante]');
        if (botao) abrirDialog(botao);
    });

    btnFechar?.addEventListener('click', fecharDialog);
    dialog.addEventListener('cancel', fecharDialog);
    dialog.addEventListener('click', (evento) => {
        const area = dialog.getBoundingClientRect();
        const foraDoConteudo = evento.clientX < area.left || evento.clientX > area.right
            || evento.clientY < area.top || evento.clientY > area.bottom;
        if (foraDoConteudo) fecharDialog();
    });
})();
