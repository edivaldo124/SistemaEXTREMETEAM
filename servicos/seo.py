"""SEO técnico das páginas públicas: robots.txt, sitemap, URL canônica e schema.org.

Nada aqui toca área autenticada: as páginas logadas saem do índice pelo `noindex` dos
layouts aluno/admin/professor, e o robots.txt só pede para não rastreá-las.
"""

import re
import unicodedata
from xml.sax.saxutils import escape

from flask import request, url_for

from servicos.urls import URLPublicaInvalida, base_url_publica

NOME_ACADEMIA = 'Centro de Treinamento Extreme Team'
IMAGEM_COMPARTILHAMENTO = 'imagens/og-extreme-team.jpg'
LOGO = 'imagens/logo-icon.png'

# Endpoints que vão para o sitemap: só páginas públicas e estáveis. Páginas com token
# (ativar acesso, nova senha) e a de obrigado ficam de fora e levam `noindex`.
ENDPOINTS_SITEMAP = (
    'home',
    'auth.pagina_cadastro',
    'auth.pagina_login',
    'auth.recuperar_senha',
    'auth.termos_de_servico',
    'auth.politica_privacidade',
    'auth.pagina_termos_responsabilidade',
)

# Áreas autenticadas e rotas técnicas. O `Allow` de /professores/ vence o `Disallow` de
# /professor (a regra mais longa ganha) e mantém as fotos públicas da equipe rastreáveis.
CAMINHOS_BLOQUEADOS = (
    '/admin', '/perfil', '/api', '/professor', '/turmas', '/checkout', '/pix',
    '/logout', '/health', '/ativar-acesso/', '/recuperar_senha/', '/cadastro/obrigado',
)
CAMINHOS_LIBERADOS = ('/professores/',)


def origem_publica():
    """APP_BASE_URL quando configurada; senão a origem da requisição (o Host já passou
    por TRUSTED_HOSTS), para o desenvolvimento local continuar com URLs absolutas."""
    try:
        return base_url_publica()
    except URLPublicaInvalida:
        return request.url_root.rstrip('/')


def url_absoluta(endpoint, **valores):
    return f'{origem_publica()}{url_for(endpoint, **valores)}'


def url_estatico(arquivo):
    return url_absoluta('static', filename=arquivo)


def pagina_indexavel():
    """Só as rotas do sitemap vão para o índice. A decisão é pela rota, não pelo
    template: `recuperar.html` também responde em /recuperar_senha/<token>, e um
    canonical ali publicaria o token."""
    return request.endpoint in ENDPOINTS_SITEMAP


def url_canonica():
    # Sem query string: filtros, âncoras e parâmetros de campanha não viram páginas novas.
    return f'{origem_publica()}{request.path}'


def conteudo_robots():
    linhas = ['User-agent: *']
    linhas += [f'Allow: {caminho}' for caminho in CAMINHOS_LIBERADOS]
    linhas += [f'Disallow: {caminho}' for caminho in CAMINHOS_BLOQUEADOS]
    linhas += ['', f'Sitemap: {url_absoluta("seo.sitemap")}', '']
    return '\n'.join(linhas)


def conteudo_sitemap():
    urls = ''.join(
        f'  <url><loc>{escape(url_absoluta(endpoint))}</loc></url>\n'
        for endpoint in ENDPOINTS_SITEMAP
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'{urls}'
        '</urlset>\n'
    )


# --- Horários: texto livre do painel -> OpeningHoursSpecification -------------------
#
# O administrador escreve os horários à mão ("uma linha para cada dia ou intervalo de
# dias"). Só as linhas num formato reconhecível viram dado estruturado; o resto é
# omitido, porque um horário inventado no Google é pior do que nenhum.

_DIAS = {
    'seg': 'Monday', 'segunda': 'Monday',
    'ter': 'Tuesday', 'terca': 'Tuesday',
    'qua': 'Wednesday', 'quarta': 'Wednesday',
    'qui': 'Thursday', 'quinta': 'Thursday',
    'sex': 'Friday', 'sexta': 'Friday',
    'sab': 'Saturday', 'sabado': 'Saturday',
    'dom': 'Sunday', 'domingo': 'Sunday',
}
_ORDEM_DIAS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
_HORA = r'(\d{1,2})(?:\s*[:h]\s*(\d{2}))?\s*h?'
_INTERVALO = re.compile(_HORA + r'\s*(?:as|a|ate|-)\s*' + _HORA)


def _sem_acento(texto):
    texto = unicodedata.normalize('NFKD', texto.lower())
    return ''.join(c for c in texto if not unicodedata.combining(c))


def _dia(palavra):
    palavra = palavra.strip(' .:')
    palavra = re.sub(r'-feira$', '', palavra)
    return _DIAS.get(palavra)


def _dias_da_linha(trecho):
    trecho = re.sub(r'[–—]', '-', trecho).strip(' :')
    # "seg a sex", "segunda-feira até sexta-feira", "seg-sex". O separador exige espaço
    # em volta do "a" para "sabado" não virar a faixa "s" a "bado".
    faixa = re.fullmatch(r'([a-z.]+(?:-feira)?)(?:\s+(?:a|ate)\s+|\s*-\s*)([a-z.]+(?:-feira)?)', trecho)
    if faixa:
        inicio, fim = _dia(faixa.group(1)), _dia(faixa.group(2))
        if not inicio or not fim:
            return None
        i, f = _ORDEM_DIAS.index(inicio), _ORDEM_DIAS.index(fim)
        if i > f:
            return None
        return _ORDEM_DIAS[i:f + 1]
    dias = [_dia(parte) for parte in re.split(r'\s*(?:,|\se\s|/)\s*', trecho) if parte.strip()]
    if not dias or not all(dias):
        return None
    return dias


def _hora(horas, minutos):
    horas, minutos = int(horas), int(minutos or 0)
    if horas == 24 and minutos == 0:
        return '23:59'
    if horas > 23 or minutos > 59:
        return None
    return f'{horas:02d}:{minutos:02d}'


def horarios_estruturados(texto):
    especificacoes = []
    for linha in (texto or '').splitlines():
        linha = _sem_acento(linha).replace('–', '-').replace('—', '-')
        primeiro_digito = re.search(r'\d', linha)
        if not primeiro_digito or 'fechado' in linha:
            continue
        dias = _dias_da_linha(linha[:primeiro_digito.start()])
        if not dias:
            continue
        for intervalo in _INTERVALO.finditer(linha[primeiro_digito.start():]):
            abre = _hora(intervalo.group(1), intervalo.group(2))
            fecha = _hora(intervalo.group(3), intervalo.group(4))
            if abre and fecha:
                especificacoes.append({
                    '@type': 'OpeningHoursSpecification',
                    'dayOfWeek': dias,
                    'opens': abre,
                    'closes': fecha,
                })
    return especificacoes


def dados_estruturados_academia(academia):
    """JSON-LD ExerciseGym da home. Campo sem valor não entra (nem vazio, nem null)."""
    dados = {
        '@context': 'https://schema.org',
        '@type': 'ExerciseGym',
        'name': NOME_ACADEMIA,
        'url': url_absoluta('home'),
        'logo': url_estatico(LOGO),
        'image': url_estatico(IMAGEM_COMPARTILHAMENTO),
    }
    if academia is None:
        return dados

    if academia.endereco:
        rua = academia.endereco
        if academia.complemento:
            rua = f'{rua}, {academia.complemento}'
        dados['address'] = {
            '@type': 'PostalAddress',
            'streetAddress': rua,
            'addressCountry': 'BR',
        }
        dados['hasMap'] = academia.mapa_url
    if academia.whatsapp:
        dados['telephone'] = f'+{academia.whatsapp}'
    if academia.email:
        dados['email'] = academia.email
    if academia.instagram_url:
        dados['sameAs'] = [academia.instagram_url]
    horarios = horarios_estruturados(academia.horarios)
    if horarios:
        dados['openingHoursSpecification'] = horarios
    return dados
