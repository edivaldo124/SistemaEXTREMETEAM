// Lembrar usuário (static/js/auth.js, na tela de login e no modal da home): o usuário e o
// e-mail ficam no aparelho para o próximo acesso. O CPF também faz login, mas não é guardado
// (LGPD), e um CPF guardado antes desta regra sai do aparelho na próxima vez que a tela abre.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const CODIGO = fs.readFileSync(path.join(__dirname, '../../static/js/auth.js'), 'utf8');

// `modal`: os ids do modal de login da home, que usa o mesmo script.
function montar({ salvo = null, valor = '', lembrar = true, modal = false } = {}) {
    const ouvintes = {};
    const armazenado = new Map(salvo === null ? [] : [['et_lembrar_usuario', salvo]]);
    const campo = { value: valor, checked: false };
    const check = { checked: lembrar };
    const idCampo = modal ? 'inputnome' : 'loginusuario';
    const idLembrar = modal ? 'modal_lembrar_usuario' : 'lembrar_usuario';
    const elementos = { [idCampo]: campo, [idLembrar]: check };
    const formulario = {
        querySelector: (seletor) => ({ [`#${idLembrar}`]: check, [`#${idCampo}`]: campo })[seletor] || null,
    };
    const document = {
        addEventListener: (tipo, funcao) => { (ouvintes[tipo] = ouvintes[tipo] || []).push(funcao); },
        getElementById: (id) => elementos[id] || null,
        querySelectorAll: () => [],
    };
    const localStorage = {
        getItem: (chave) => (armazenado.has(chave) ? armazenado.get(chave) : null),
        setItem: (chave, valorGuardado) => armazenado.set(chave, String(valorGuardado)),
        removeItem: (chave) => armazenado.delete(chave),
    };
    vm.runInNewContext(CODIGO, { document, localStorage, window: { matchMedia: () => ({ matches: false }) } });

    return {
        armazenado,
        campo,
        carregar() { ouvintes.DOMContentLoaded.forEach((funcao) => funcao({})); },
        enviar() { ouvintes.submit.forEach((funcao) => funcao({ target: formulario })); },
    };
}

test('o usuário digitado fica guardado para o próximo acesso', () => {
    const tela = montar({ valor: 'edi.aluno' });
    tela.carregar();
    tela.enviar();
    assert.equal(tela.armazenado.get('et_lembrar_usuario'), 'edi.aluno');
});

test('o e-mail também fica guardado', () => {
    const tela = montar({ valor: 'aluno@example.com' });
    tela.carregar();
    tela.enviar();
    assert.equal(tela.armazenado.get('et_lembrar_usuario'), 'aluno@example.com');
});

test('CPF digitado não fica guardado no aparelho, com ou sem máscara', () => {
    for (const valor of ['123.456.789-01', '12345678901']) {
        const tela = montar({ valor });
        tela.carregar();
        tela.enviar();
        assert.equal(tela.armazenado.has('et_lembrar_usuario'), false, valor);
    }
});

test('o modal da home segue a mesma regra: guarda o usuário e nunca o CPF', () => {
    const usuario = montar({ modal: true, valor: 'edi.aluno' });
    usuario.carregar();
    usuario.enviar();
    assert.equal(usuario.armazenado.get('et_lembrar_usuario'), 'edi.aluno');

    const cpf = montar({ modal: true, valor: '123.456.789-01' });
    cpf.carregar();
    cpf.enviar();
    assert.equal(cpf.armazenado.has('et_lembrar_usuario'), false);
});

test('CPF guardado antes da regra sai do aparelho ao abrir a tela', () => {
    const tela = montar({ salvo: '12345678901' });
    tela.carregar();
    assert.equal(tela.armazenado.has('et_lembrar_usuario'), false);
    assert.equal(tela.campo.value, '');
});
