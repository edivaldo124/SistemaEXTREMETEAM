(() => {
    const dialog = document.getElementById('turma-dialog');
    if (!dialog) return;

    const elNome = dialog.querySelector('[data-turma-nome-titulo]');
    const elProfessor = dialog.querySelector('[data-turma-professor-valor]');
    const elDias = dialog.querySelector('[data-turma-dias-valor]');
    const elHorario = dialog.querySelector('[data-turma-horario-valor]');
    const btnFechar = dialog.querySelector('[data-turma-fechar]');

    let elementoAnterior = null;

    function abrir(botao) {
        elementoAnterior = document.activeElement;
        elNome.textContent = botao.dataset.turmaNome || '—';
        elProfessor.textContent = botao.dataset.turmaProfessor || '—';
        elDias.textContent = botao.dataset.turmaDias || '—';
        elHorario.textContent = botao.dataset.turmaHorario || '—';
        dialog.showModal();
    }

    function fechar() {
        if (dialog.open) dialog.close();
        if (elementoAnterior) elementoAnterior.focus();
    }

    document.addEventListener('click', (evento) => {
        const botao = evento.target.closest('[data-abrir-turma]');
        if (botao) abrir(botao);
    });

    btnFechar?.addEventListener('click', fechar);
    dialog.addEventListener('cancel', fechar);
    dialog.addEventListener('click', (evento) => {
        const area = dialog.getBoundingClientRect();
        const fora = evento.clientX < area.left || evento.clientX > area.right
            || evento.clientY < area.top || evento.clientY > area.bottom;
        if (fora) fechar();
    });
})();
