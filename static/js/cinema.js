// Hero cinematográfico da página inicial (padrão Framerate). A rolagem dentro de
// .cinema é o "filme": o progresso de 0 a 1 troca as manchetes, enche o medidor e
// move a cena 3D. A cena (front/, React Three Fiber) só é baixada depois que a
// página carregou e nunca com movimento reduzido, economia de dados ou sem WebGL:
// nesses casos fica o pôster estático. Aparelho com pouca memória recebe a mesma cena,
// mais leve.

(function () {
  'use strict';

  const secao = document.querySelector('[data-cinema]');
  if (!secao) return;

  const manchetes = Array.from(secao.querySelectorAll('[data-cinema-manchete]'));
  const preenchimento = secao.querySelector('[data-cinema-medidor-preenchimento]');
  const valor = secao.querySelector('[data-cinema-medidor-valor]');
  const alvoCena = secao.querySelector('[data-cinema-cena]');
  const carregando = document.querySelector('[data-cinema-carregando]');
  const reduzir = window.matchMedia('(prefers-reduced-motion: reduce)');
  // A cena lê daqui a cada quadro (front/src/estado.ts).
  const estado = (window.etCinema = { progresso: 0, indice: 0, total: manchetes.length });

  // ------------------------------------------------- manchetes e medidor --
  function ativar(indice) {
    manchetes.forEach(function (manchete, i) {
      manchete.classList.toggle('is-active', i === indice);
      manchete.classList.toggle('is-before', i < indice);
      manchete.classList.toggle('is-after', i > indice);
      // As escondidas saem do leitor de tela e da ordem do Tab (o link de cada uma
      // continuaria focável, invisível, sem o inert).
      if (i === indice) manchete.removeAttribute('aria-hidden');
      else manchete.setAttribute('aria-hidden', 'true');
      manchete.inert = i !== indice;
    });
  }

  let agendado = false;
  function medir() {
    agendado = false;
    const caixa = secao.getBoundingClientRect();
    const percurso = caixa.height - window.innerHeight;
    const progresso = percurso > 0 ? Math.min(1, Math.max(0, -caixa.top / percurso)) : 0;
    const indice = Math.min(manchetes.length - 1, Math.floor(progresso * manchetes.length));
    estado.progresso = progresso;
    // Direto no DOM, sem framework: isto roda a cada quadro de rolagem.
    if (preenchimento) preenchimento.style.transform = 'scaleY(' + Math.max(0.04, progresso).toFixed(4) + ')';
    if (valor) valor.textContent = String(Math.round(progresso * 100)).padStart(2, '0');
    if (indice !== estado.indice) {
      estado.indice = indice;
      ativar(indice);
    }
    window.dispatchEvent(new CustomEvent('cinema:progresso', { detail: { progresso: progresso, indice: indice } }));
  }
  function pedirMedida() {
    if (agendado) return;
    agendado = true;
    window.requestAnimationFrame(medir);
  }
  window.addEventListener('scroll', pedirMedida, { passive: true });
  window.addEventListener('resize', pedirMedida);
  medir();

  // -------------------------------------------------------------- loader --
  // Só na primeira visita da aba; o CSS o esconde sozinho depois de 4,5 s se este
  // arquivo falhar. Aqui ele sai quando a página, as fontes e a cena estão prontas,
  // ou em 3 s, o que vier primeiro.
  function concluirCarregamento() {
    secao.classList.add('cinema--pronto');
    if (!carregando || carregando.classList.contains('is-complete')) return;
    carregando.classList.add('is-complete');
    try { sessionStorage.setItem('et-cinema-visto', '1'); } catch (e) { /* aba privada */ }
  }

  const paginaPronta = new Promise(function (resolver) {
    if (document.readyState === 'complete') resolver();
    else window.addEventListener('load', resolver, { once: true });
  }).then(function () {
    return document.fonts ? document.fonts.ready : null;
  });

  // ---------------------------------------------------------------- cena --
  function podeTer3D() {
    if (reduzir.matches) return false;
    const conexao = navigator.connection;
    if (conexao && (conexao.saveData || /(^|-)2g$/.test(conexao.effectiveType || ''))) return false;
    try {
      const teste = document.createElement('canvas');
      // Sem aceleração de vídeo (renderização por software) a cena travaria a página.
      const opcoes = { failIfMajorPerformanceCaveat: true };
      const contexto = teste.getContext('webgl2', opcoes) || teste.getContext('webgl', opcoes);
      if (!contexto) return false;
      // O navegador limita os contextos WebGL abertos: devolve o do teste.
      const perder = contexto.getExtension('WEBGL_lose_context');
      if (perder) perder.loseContext();
      return true;
    } catch (e) {
      return false;
    }
  }

  function carregarCena() {
    const video = secao.getAttribute('data-video-src');
    const modulo = video ? secao.getAttribute('data-video-modulo') : secao.getAttribute('data-cena-src');
    if (!alvoCena || !modulo || !podeTer3D()) return Promise.resolve(false);
    return new Promise(function (resolver) {
      const opcoes = {
        estreito: window.matchMedia('(max-width: 720px)').matches,
        // Menos de 4 GB (o Chrome arredonda para baixo, então 3 GB também cai aqui).
        leve: !!navigator.deviceMemory && navigator.deviceMemory < 4,
        eventSource: secao,
        aoFicarPronta: function () {
          secao.classList.add('cinema--cena-pronta');
          resolver(true);
        },
        // Contexto WebGL perdido (aba em segundo plano no celular, driver): o pôster volta.
        aoPerderContexto: function () {
          secao.classList.remove('cinema--cena-pronta');
        },
      };
      import(modulo)
        .then(function (m) {
          return video ? m.montar(alvoCena, video, opcoes) : m.montar(alvoCena, opcoes);
        })
        .catch(function () { resolver(false); });
    });
  }

  // A cena espera a página: não disputa banda nem CPU com o primeiro conteúdo.
  const cenaPronta = paginaPronta.then(function () {
    return new Promise(function (resolver) {
      const ocioso = window.requestIdleCallback || function (fn) { return setTimeout(fn, 200); };
      ocioso(function () { carregarCena().then(resolver); }, { timeout: 1500 });
    });
  });
  const vigia = new Promise(function (resolver) { setTimeout(resolver, 3000); });
  Promise.all([paginaPronta, Promise.race([cenaPronta, vigia])]).then(concluirCarregamento);
})();
