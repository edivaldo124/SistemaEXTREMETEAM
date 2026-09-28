// Google Analytics 4 com consentimento (servicos/analytics.py e
// components/consentimento_analytics.html). Nada vai para o Google antes do
// "Aceitar": o gtag.js só é baixado depois dele. A escolha fica neste navegador e
// pode ser trocada em "Preferências de cookies", no rodapé. Recusar depois de aceitar
// desliga a coleta e apaga os cookies _ga deste domínio.
//
// Nada que identifique a pessoa sai daqui: o endereço vai sem query string (nunca um
// token ou parâmetro), a origem vai só com o domínio, e o único evento próprio é o de
// cadastro concluído, sem parâmetro pessoal.

(function () {
  'use strict';

  const script = document.currentScript;
  const ID = script && script.dataset.analyticsId;
  if (!ID) return;
  const EVENTO = script.dataset.evento || '';
  const CHAVE = 'et-consentimento-analytics';
  const VERSAO = 1;
  const banner = document.querySelector('[data-consentimento]');

  function lerEscolha() {
    try {
      const salvo = JSON.parse(window.localStorage.getItem(CHAVE));
      return salvo && salvo.versao === VERSAO ? salvo.escolha : null;
    } catch (_erro) {
      return null;
    }
  }

  function gravarEscolha(escolha) {
    try {
      window.localStorage.setItem(CHAVE, JSON.stringify({ versao: VERSAO, escolha }));
    } catch (_erro) {
      // Sem armazenamento (aba anônima, bloqueio): vale só para esta página.
    }
  }

  function origemDoReferrer() {
    try {
      return document.referrer ? new URL(document.referrer).origin + '/' : '';
    } catch (_erro) {
      return '';
    }
  }

  let carregado = false;
  function carregar() {
    window[`ga-disable-${ID}`] = false;
    if (carregado) {
      // Aceitou de novo depois de recusar nesta mesma página.
      window.gtag('consent', 'update', { analytics_storage: 'granted' });
      return;
    }
    carregado = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function gtag() { window.dataLayer.push(arguments); };
    window.gtag('consent', 'default', {
      analytics_storage: 'granted',
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied',
    });
    window.gtag('js', new Date());
    window.gtag('config', ID, {
      page_location: window.location.origin + window.location.pathname,
      page_referrer: origemDoReferrer(),
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
    });
    if (EVENTO) window.gtag('event', EVENTO, { method: 'site' });

    const gtagJs = document.createElement('script');
    gtagJs.async = true;
    gtagJs.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(ID)}`;
    document.head.appendChild(gtagJs);
  }

  function apagarCookiesGa() {
    const partes = window.location.hostname.split('.');
    // O GA grava no domínio registrável (".exemplo.com.br"); tenta cada sufixo.
    const dominios = [''];
    for (let i = 0; i < partes.length - 1; i += 1) dominios.push(`.${partes.slice(i).join('.')}`);
    document.cookie.split(';')
      .map((par) => par.split('=')[0].trim())
      .filter((nome) => nome === '_ga' || nome.startsWith('_ga_') || nome === '_gid')
      .forEach((nome) => {
        dominios.forEach((dominio) => {
          document.cookie = `${nome}=; Max-Age=0; path=/${dominio ? `; domain=${dominio}` : ''}`;
        });
      });
  }

  function revogar() {
    window[`ga-disable-${ID}`] = true;
    if (typeof window.gtag === 'function') {
      window.gtag('consent', 'update', { analytics_storage: 'denied' });
    }
    apagarCookiesGa();
  }

  function mostrarAviso(focar) {
    if (!banner) return;
    banner.hidden = false;
    if (focar) {
      const primeiro = banner.querySelector('button');
      if (primeiro) primeiro.focus();
    }
  }

  function esconderAviso() {
    if (banner) banner.hidden = true;
  }

  document.addEventListener('click', (evento) => {
    const alvo = evento.target;
    if (!(alvo instanceof Element)) return;
    if (alvo.closest('[data-consentimento-aceitar]')) {
      gravarEscolha('aceito');
      esconderAviso();
      carregar();
    } else if (alvo.closest('[data-consentimento-recusar]')) {
      gravarEscolha('recusado');
      esconderAviso();
      revogar();
    } else if (alvo.closest('[data-consentimento-abrir]')) {
      mostrarAviso(true);
    }
  });

  const escolha = lerEscolha();
  if (escolha === 'aceito') carregar();
  else if (escolha === null) mostrarAviso(false);
}());
