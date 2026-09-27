// Comportamento dos componentes de templates/components/ (carregado em todas as
// páginas por layouts/base.html). Só addEventListener e data-atributos: a CSP
// bloqueia handler inline.

(function () {
  'use strict';

  // ---------------------------------------------------------------- toast --
  const TOAST_TEMPO_MS = 6000;
  // Mesmos traços de components/toasts.html.
  const TOAST_ICONES = {
    erro: 'M12 8v5m0 3.5v.5M10.3 3.9 2.4 18a2 2 0 0 0 1.7 3h15.8a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z',
    aviso: 'M12 8v5m0 3.5v.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z',
    sucesso: 'm7.5 12.5 3 3 6-7M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z',
    info: 'M12 11v6m0-9.5V7M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z',
  };
  const semMovimento = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function fecharToast(toast) {
    if (!toast || toast.classList.contains('saindo')) return;
    clearTimeout(toast._timer);
    if (semMovimento()) { toast.remove(); return; }
    toast.classList.add('saindo');
    toast.addEventListener('animationend', () => toast.remove(), { once: true });
  }

  function agendarSaida(toast) {
    if (!toast.hasAttribute('data-toast-some')) return;
    const iniciar = () => { clearTimeout(toast._timer); toast._timer = setTimeout(() => fecharToast(toast), TOAST_TEMPO_MS); };
    const pausar = () => clearTimeout(toast._timer);
    toast.addEventListener('mouseenter', pausar);
    toast.addEventListener('mouseleave', iniciar);
    toast.addEventListener('focusin', pausar);
    toast.addEventListener('focusout', iniciar);
    iniciar();
  }

  function prepararToast(toast) {
    const botao = toast.querySelector('[data-toast-fechar]');
    if (botao) botao.addEventListener('click', () => fecharToast(toast));
    agendarSaida(toast);
  }

  // Aviso criado pelo próprio front (ex.: "Código copiado"). Mesmo markup do servidor.
  window.etToast = function (texto, categoria) {
    const regiao = document.querySelector('[data-toasts]');
    if (!regiao) return;
    const tipo = ['erro', 'aviso', 'sucesso', 'info'].includes(categoria) ? categoria : 'info';
    const toast = document.createElement('div');
    toast.className = `et-toast et-toast--${tipo}`;
    toast.setAttribute('role', tipo === 'erro' ? 'alert' : 'status');
    toast.setAttribute('data-toast', '');
    if (tipo !== 'erro') toast.setAttribute('data-toast-some', '');
    const p = document.createElement('p');
    p.textContent = texto;
    const fechar = document.createElement('button');
    fechar.type = 'button';
    fechar.className = 'et-toast-fechar';
    fechar.setAttribute('data-toast-fechar', '');
    fechar.setAttribute('aria-label', 'Fechar aviso');
    fechar.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18" /></svg>';
    const icone = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    icone.setAttribute('viewBox', '0 0 24 24');
    icone.setAttribute('aria-hidden', 'true');
    icone.innerHTML = `<path d="${TOAST_ICONES[tipo]}" />`;
    toast.append(icone, p, fechar);
    regiao.append(toast);
    prepararToast(toast);
    return toast;
  };

  document.querySelectorAll('[data-toast]').forEach(prepararToast);

  document.addEventListener('keydown', (evento) => {
    if (evento.key !== 'Escape') return;
    const toast = document.activeElement && document.activeElement.closest('[data-toast]');
    if (toast) fecharToast(toast);
  });

  // ----------------------------------------------------------------- tabs --
  // Padrão WAI-ARIA com ativação automática: setas trocam de aba, Home/End vão
  // às pontas. Só a aba ativa entra na ordem de Tab.
  document.querySelectorAll('[data-tabs]').forEach((grupo) => {
    const abas = Array.from(grupo.querySelectorAll('[role="tab"]'));
    function ativar(aba, focar) {
      abas.forEach((item) => {
        const ativa = item === aba;
        item.setAttribute('aria-selected', ativa ? 'true' : 'false');
        item.tabIndex = ativa ? 0 : -1;
        const painel = document.getElementById(item.getAttribute('aria-controls'));
        if (painel) painel.hidden = !ativa;
      });
      if (focar) aba.focus();
    }
    abas.forEach((aba, i) => {
      aba.addEventListener('click', () => ativar(aba, false));
      aba.addEventListener('keydown', (evento) => {
        const destino = {
          ArrowRight: abas[(i + 1) % abas.length],
          ArrowLeft: abas[(i - 1 + abas.length) % abas.length],
          Home: abas[0],
          End: abas[abas.length - 1],
        }[evento.key];
        if (!destino) return;
        evento.preventDefault();
        ativar(destino, true);
      });
    });
  });

  // ------------------------------------------------------- menu de ações --
  let menuAberto = null;

  function fecharMenu(devolverFoco) {
    if (!menuAberto) return;
    const { botao, lista } = menuAberto;
    botao.setAttribute('aria-expanded', 'false');
    lista.hidden = true;
    if (devolverFoco) botao.focus();
    menuAberto = null;
  }

  document.querySelectorAll('[data-menu]').forEach((menu) => {
    const botao = menu.querySelector('[aria-haspopup="menu"]');
    const lista = menu.querySelector('[role="menu"]');
    if (!botao || !lista) return;
    const itens = () => Array.from(lista.querySelectorAll('[role="menuitem"]'));

    function abrir(focarUltimo) {
      if (menuAberto && menuAberto.lista !== lista) fecharMenu(false);
      botao.setAttribute('aria-expanded', 'true');
      lista.hidden = false;
      menuAberto = { botao, lista };
      // Dentro de um contêiner com rolagem própria (tabela), a lista absoluta seria
      // cortada pela borda dele: nesse caso ela flutua presa ao botão (position:fixed).
      lista.style.position = lista.style.top = lista.style.left = lista.style.right = '';
      if (botao.closest('.et-tabela-rolagem')) {
        const caixa = botao.getBoundingClientRect();
        lista.style.position = 'fixed';
        lista.style.right = 'auto';
        const largura = lista.offsetWidth;
        const altura = lista.offsetHeight;
        const abaixo = caixa.bottom + 4 + altura <= window.innerHeight;
        lista.style.top = `${abaixo ? caixa.bottom + 4 : Math.max(8, caixa.top - 4 - altura)}px`;
        lista.style.left = `${Math.max(8, Math.min(caixa.right - largura, window.innerWidth - largura - 8))}px`;
      } else {
        // Abre alinhada à direita do botão; se assim sairia da tela, alinha à esquerda.
        lista.classList.remove('et-menu-lista--esquerda');
        if (lista.getBoundingClientRect().left < 8) lista.classList.add('et-menu-lista--esquerda');
      }
      const lista_ = itens();
      if (lista_.length) (focarUltimo ? lista_[lista_.length - 1] : lista_[0]).focus();
    }

    botao.addEventListener('click', () => {
      if (botao.getAttribute('aria-expanded') === 'true') fecharMenu(false);
      else abrir(false);
    });
    botao.addEventListener('keydown', (evento) => {
      if (evento.key === 'ArrowDown') { evento.preventDefault(); abrir(false); }
      if (evento.key === 'ArrowUp') { evento.preventDefault(); abrir(true); }
    });
    lista.addEventListener('keydown', (evento) => {
      const lista_ = itens();
      const i = lista_.indexOf(document.activeElement);
      const destino = {
        ArrowDown: lista_[(i + 1) % lista_.length],
        ArrowUp: lista_[(i - 1 + lista_.length) % lista_.length],
        Home: lista_[0],
        End: lista_[lista_.length - 1],
      }[evento.key];
      if (destino) { evento.preventDefault(); destino.focus(); }
      if (evento.key === 'Tab') fecharMenu(false);
    });
  });

  document.addEventListener('click', (evento) => {
    if (menuAberto && !menuAberto.lista.parentElement.contains(evento.target)) fecharMenu(false);
  });

  // --------------------------------------------------------------- tooltip --
  // O texto vem do aria-label, que já é o nome acessível: o balão é só visual
  // (aria-hidden) para o leitor de tela não repetir o rótulo.
  let tooltip = null;
  let alvoTooltip = null;

  function mostrarTooltip(alvo) {
    const texto = alvo.getAttribute('aria-label');
    if (!texto) return;
    if (!tooltip) {
      tooltip = document.createElement('span');
      tooltip.className = 'et-tooltip';
      tooltip.setAttribute('role', 'tooltip');
      tooltip.setAttribute('aria-hidden', 'true');
      document.body.append(tooltip);
    }
    alvoTooltip = alvo;
    tooltip.textContent = texto;
    tooltip.classList.add('et-tooltip--visivel');
    const caixa = alvo.getBoundingClientRect();
    const balao = tooltip.getBoundingClientRect();
    const MARGEM = 8;
    let topo = caixa.top - balao.height - MARGEM;
    let abaixo = false;
    if (topo < MARGEM) { topo = caixa.bottom + MARGEM; abaixo = true; }
    let esquerda = caixa.left + caixa.width / 2 - balao.width / 2;
    esquerda = Math.max(MARGEM, Math.min(esquerda, window.innerWidth - balao.width - MARGEM));
    tooltip.style.top = `${topo + window.scrollY}px`;
    tooltip.style.left = `${esquerda + window.scrollX}px`;
    tooltip.classList.toggle('et-tooltip--abaixo', abaixo);
  }

  function esconderTooltip() {
    if (tooltip) tooltip.classList.remove('et-tooltip--visivel');
    alvoTooltip = null;
  }

  document.querySelectorAll('[data-tooltip]').forEach((alvo) => {
    alvo.addEventListener('mouseenter', () => mostrarTooltip(alvo));
    alvo.addEventListener('focus', () => mostrarTooltip(alvo));
    alvo.addEventListener('mouseleave', esconderTooltip);
    alvo.addEventListener('blur', esconderTooltip);
  });
  window.addEventListener('scroll', () => { if (alvoTooltip) esconderTooltip(); }, { passive: true });
  // Menu flutuante (position:fixed) não acompanha a rolagem: fecha em vez de descolar do botão.
  document.addEventListener('scroll', () => {
    if (menuAberto && menuAberto.lista.style.position === 'fixed') fecharMenu(false);
  }, { passive: true, capture: true });

  // ------------------------------------------------ botão com carregamento --
  // Escuta no document: os handlers do próprio form (ex.: a confirmação do
  // modal.js) rodam antes e, se cancelarem o envio, o botão não trava.
  document.addEventListener('submit', (evento) => {
    const form = evento.target;
    if (evento.defaultPrevented || !form.matches('[data-enviando]')) return;
    const botao = evento.submitter && form.contains(evento.submitter)
      ? evento.submitter
      : form.querySelector('[type="submit"]');
    if (!botao || botao.disabled) return;
    // O nome/valor do botão clicado continua indo no envio mesmo desabilitado.
    if (botao.name) {
      const campo = document.createElement('input');
      campo.type = 'hidden';
      campo.name = botao.name;
      campo.value = botao.value;
      campo.dataset.enviandoCopia = '';
      form.append(campo);
    }
    botao.dataset.textoOriginal = botao.textContent;
    botao.textContent = botao.dataset.textoEnviando || 'Enviando...';
    botao.classList.add('et-carregando');
    botao.setAttribute('aria-busy', 'true');
    // Desabilita depois do envio começar: desabilitar dentro do submit tiraria o botão do formulário enviado.
    setTimeout(() => { botao.disabled = true; }, 0);
  });

  // Voltar pelo histórico (bfcache) devolve a página congelada com o botão travado.
  window.addEventListener('pageshow', (evento) => {
    if (!evento.persisted) return;
    document.querySelectorAll('.et-carregando[aria-busy="true"]').forEach((botao) => {
      botao.disabled = false;
      botao.removeAttribute('aria-busy');
      botao.classList.remove('et-carregando');
      if (botao.dataset.textoOriginal) botao.textContent = botao.dataset.textoOriginal;
    });
    document.querySelectorAll('[data-enviando-copia]').forEach((campo) => campo.remove());
  });

  // ------------------------------------------------------ tabela de dados --
  // Busca e ordenação só no que já está na tela: use só em tabelas sem paginação.
  const comparar = new Intl.Collator('pt-BR', { sensitivity: 'base', numeric: true }).compare;

  function valorCelula(linha, coluna, tipo) {
    const celula = linha.cells[coluna];
    const bruto = celula ? (celula.dataset.valor ?? celula.textContent.trim()) : '';
    if (tipo === 'numero') {
      const n = Number(String(bruto).replace(/[^\d,.-]/g, '').replace(/\.(?=\d{3}(\D|$))/g, '').replace(',', '.'));
      return Number.isNaN(n) ? -Infinity : n;
    }
    if (tipo === 'data') {
      const m = String(bruto).match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
      return m ? `${m[3]}-${m[2]}-${m[1]}` : String(bruto);
    }
    return String(bruto);
  }

  document.querySelectorAll('[data-tabela]').forEach((bloco) => {
    const tabela = bloco.querySelector('table');
    const corpo = tabela && tabela.tBodies[0];
    if (!corpo) return;
    const busca = bloco.querySelector('[data-tabela-busca]');
    const vazio = bloco.querySelector('[data-tabela-vazio]');

    tabela.querySelectorAll('th [data-ordenar]').forEach((botao) => {
      const th = botao.closest('th');
      botao.addEventListener('click', () => {
        const coluna = th.cellIndex;
        const tipo = botao.dataset.ordenar;
        const crescente = th.getAttribute('aria-sort') !== 'ascending';
        tabela.querySelectorAll('th[aria-sort]').forEach((outro) => outro.setAttribute('aria-sort', 'none'));
        th.setAttribute('aria-sort', crescente ? 'ascending' : 'descending');
        const linhas = Array.from(corpo.rows);
        linhas.sort((a, b) => {
          const va = valorCelula(a, coluna, tipo);
          const vb = valorCelula(b, coluna, tipo);
          const r = tipo === 'numero' ? va - vb : comparar(va, vb);
          return crescente ? r : -r;
        });
        corpo.append(...linhas);
      });
    });

    if (busca) {
      const normalizar = (t) => t.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
      busca.addEventListener('input', () => {
        const termo = normalizar(busca.value.trim());
        let visiveis = 0;
        Array.from(corpo.rows).forEach((linha) => {
          const mostra = !termo || normalizar(linha.textContent).includes(termo);
          linha.hidden = !mostra;
          if (mostra) visiveis += 1;
        });
        if (vazio) vazio.hidden = visiveis > 0;
      });
    }
  });

  // ------------------------------------------- upload com pré-visualização --
  // Validação de conveniência: tipo e tamanho são conferidos de novo no servidor.
  const formatoTamanho = new Intl.NumberFormat('pt-BR', { maximumFractionDigits: 1 });
  const listaFormatos = (tipos) => new Intl.ListFormat('pt-BR', { type: 'disjunction' })
    .format(tipos.map((t) => (t === 'image/jpeg' ? 'JPG' : t.split('/')[1].toUpperCase())));

  document.querySelectorAll('[data-upload]').forEach((bloco) => {
    const campo = bloco.querySelector('input[type="file"]');
    const previa = bloco.querySelector('[data-upload-previa]');
    const erro = bloco.querySelector('[data-upload-erro]');
    const alvo = bloco.querySelector('.et-upload-alvo');
    if (!campo) return;
    const tipos = (bloco.dataset.tipos || '').split(',').map((t) => t.trim()).filter(Boolean);
    const maxBytes = Number(bloco.dataset.maxMb || 0) * 1024 * 1024;
    let urlPrevia = null;

    function limpar() {
      if (urlPrevia) { URL.revokeObjectURL(urlPrevia); urlPrevia = null; }
      if (previa) { previa.replaceChildren(); previa.hidden = true; }
      bloco.classList.remove('et-upload--com-arquivo');
    }

    function mostrarErro(texto) {
      campo.value = '';
      limpar();
      if (erro) { erro.textContent = texto; erro.hidden = false; }
    }

    campo.addEventListener('change', () => {
      if (erro) { erro.hidden = true; erro.textContent = ''; }
      const arquivo = campo.files && campo.files[0];
      if (!arquivo) { limpar(); return; }
      if (tipos.length && !tipos.includes(arquivo.type)) {
        mostrarErro(`Este tipo de arquivo não é aceito. Envie ${listaFormatos(tipos)}.`);
        return;
      }
      if (maxBytes && arquivo.size > maxBytes) {
        mostrarErro(`O arquivo tem ${formatoTamanho.format(arquivo.size / 1048576)} MB. O limite é ${bloco.dataset.maxMb} MB.`);
        return;
      }
      limpar();
      if (!previa) return;
      if (arquivo.type.startsWith('image/')) {
        urlPrevia = URL.createObjectURL(arquivo);
        const img = document.createElement('img');
        img.src = urlPrevia;
        img.alt = `Pré-visualização de ${arquivo.name}`;
        previa.append(img);
      }
      const info = document.createElement('p');
      info.className = 'et-upload-arquivo';
      info.textContent = `${arquivo.name} · ${formatoTamanho.format(arquivo.size / 1048576)} MB`;
      const trocar = document.createElement('button');
      trocar.type = 'button';
      trocar.className = 'button-secondary';
      trocar.textContent = 'Trocar arquivo';
      trocar.addEventListener('click', () => campo.click());
      previa.append(info, trocar);
      previa.hidden = false;
      bloco.classList.add('et-upload--com-arquivo');
    });

    if (alvo) {
      ['dragenter', 'dragover'].forEach((tipo) => alvo.addEventListener(tipo, (evento) => {
        evento.preventDefault();
        bloco.classList.add('et-upload--arrastando');
      }));
      ['dragleave', 'drop'].forEach((tipo) => alvo.addEventListener(tipo, () => bloco.classList.remove('et-upload--arrastando')));
      alvo.addEventListener('drop', (evento) => {
        evento.preventDefault();
        if (!evento.dataTransfer || !evento.dataTransfer.files.length) return;
        campo.files = evento.dataTransfer.files;
        campo.dispatchEvent(new Event('change', { bubbles: true }));
      });
    }
  });

  // ------------------------------------------------------------- accordion --
  // <details> nativo não abre sozinho quando um link #âncora aponta para ele (ou para
  // algo dentro dele): o sumário dos termos levaria a um título recolhido.
  function abrirAlvoDaAncora() {
    if (!location.hash) return;
    let alvo = null;
    try { alvo = document.getElementById(decodeURIComponent(location.hash.slice(1))); } catch (e) { return; }
    for (let el = alvo; el; el = el.parentElement) {
      if (el.tagName === 'DETAILS') el.open = true;
    }
  }
  abrirAlvoDaAncora();
  window.addEventListener('hashchange', abrirAlvoDaAncora);

  // Esc: fecha o menu de ações (devolvendo o foco) e o tooltip.
  document.addEventListener('keydown', (evento) => {
    if (evento.key !== 'Escape') return;
    if (menuAberto) fecharMenu(true);
    esconderTooltip();
  });
})();
