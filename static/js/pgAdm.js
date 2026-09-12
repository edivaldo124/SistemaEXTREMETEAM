// A busca de alunos passou a ser feita pelo servidor (formulário GET com `busca`):
// filtrar só as linhas da página aberta escondia alunos das outras páginas e fazia o
// contador mentir. O que sobra aqui é a formatação de preços e a validação do plano.

const formularioPlano = document.getElementById('form-plano');
const campoPreco = document.getElementById('preco-plano');
const campoDuracao = document.getElementById('duracao-dias');

const formatadorDePreco = new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
});

document.querySelectorAll('.preco-plano').forEach(function (preco) {
    const valor = Number(preco.dataset.preco);

    if (!Number.isNaN(valor)) {
        preco.textContent = formatadorDePreco.format(valor);
    }
});

if (formularioPlano) {
    campoPreco.addEventListener('input', function () {
        campoPreco.setCustomValidity('');
    });

    campoDuracao.addEventListener('input', function () {
        campoDuracao.setCustomValidity('');
    });

    formularioPlano.addEventListener('submit', function (evento) {
        const preco = Number(campoPreco.value.trim().replace(',', '.'));
        const duracao = Number(campoDuracao.value);

        if (!Number.isFinite(preco) || preco <= 0) {
            evento.preventDefault();
            campoPreco.setCustomValidity('Informe um preço maior que zero.');
            campoPreco.reportValidity();
            return;
        }

        if (!Number.isInteger(duracao) || duracao <= 0) {
            evento.preventDefault();
            campoDuracao.setCustomValidity('Informe uma duração maior que zero.');
            campoDuracao.reportValidity();
            return;
        }

        campoPreco.value = preco.toFixed(2);

        const botao = formularioPlano.querySelector('.btn-cadastrar');
        botao.disabled = true;
        botao.textContent = 'Cadastrando...';
    });
}
