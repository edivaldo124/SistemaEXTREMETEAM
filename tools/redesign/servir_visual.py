"""Instância descartável para conferir o redesign no navegador (porta 4002).

SQLite em pasta temporária, nunca o banco real. As credenciais de e-mail e o token do Mercado
Pago ficam falsos/vazios de propósito: nada aqui deve sair pela rede. load_dotenv não
sobrescreve variável já definida, então definir vazio impede o .env de preencher.
"""
import os
import sys
import tempfile
from datetime import date, timedelta

from werkzeug.security import generate_password_hash

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, RAIZ)
os.chdir(RAIZ)

pasta = tempfile.mkdtemp(prefix='et-visual-')
os.environ.update(
    SECRET_KEY='chave-visual-descartavel',
    DATABASE_URL=f'sqlite:///{pasta}/visual.db',
    COOKIE_SECURE='false',
    APP_BASE_URL='http://localhost:4002',
    TRUSTED_HOSTS='localhost,127.0.0.1',
    TRUST_PROXY_COUNT='0',
    RATELIMIT_STORAGE_URI='memory://',
    UPLOAD_DIR=f'{pasta}/uploads',
    ADMIN_USER='admin',
    ADMIN_PASSWORD_HASH=generate_password_hash('admin-visual-123'),
    CRIAR_SCHEMA_NA_IMPORTACAO='true',
    FILA_EMAIL_SINCRONA='true',
    GMAIL_CLIENT_ID='',
    GMAIL_CLIENT_SECRET='',
    GMAIL_REFRESH_TOKEN='',
    GMAIL_SENDER_EMAIL='',
    MERCADO_PAGO_ACCESS_TOKEN='TEST-falso',
    MERCADO_PAGO_WEBHOOK_SECRET='falso',
    MERCADO_PAGO_CLIENT_ID='',
    MERCADO_PAGO_CLIENT_SECRET='',
    KEEP_ALIVE='false',
)

from config import db  # noqa: E402
from servidor import app  # noqa: E402
from dao.financeiroDAO import PagamentoDAO  # noqa: E402
from dao.planoDAO import PlanoDAO  # noqa: E402
from dao.usuarioDAO import AlunoDAO  # noqa: E402
from modelos.matricula import Matricula  # noqa: E402
from modelos.pagamento import Pagamento  # noqa: E402
from modelos.plano import Plano  # noqa: E402
from modelos.presenca import Presenca  # noqa: E402
from modelos.professor import Professor  # noqa: E402
from modelos.turma import Turma  # noqa: E402
from modelos.usuario import Aluno  # noqa: E402

hoje = date.today()


def aluno(i, nome, plano, **extra):
    dados = dict(
        nome=nome, login=f'aluno{i}', datanascimento='1998-04-12', cpf=f'{i:011d}',
        email=f'aluno{i}@example.com', telefone='85999990000', senha='senha123',
        descricao='', status_cadastro='aprovado', ativo=True, plano_id=plano.id,
    )
    dados.update(extra)
    a = Aluno(**dados)
    AlunoDAO.salvar(a)
    return a


def cobranca(a, plano, status, dias, **extra):
    venc = hoje + timedelta(days=dias)
    dados = dict(
        aluno_id=a.id, plano_id=plano.id, valor=plano.preco_plano, vencimento=venc,
        status=status, competencia=venc.strftime('%Y-%m'),
    )
    dados.update(extra)
    p = Pagamento(**dados)
    PagamentoDAO.salvar(p)
    return p


with app.app_context():
    mensal = Plano(nome_plano='Mensal', preco_plano=150.0, duracao_dias=30)
    trimestral = Plano(nome_plano='Trimestral', preco_plano=390.0, duracao_dias=90)
    for p in (mensal, trimestral):
        PlanoDAO.salvar(p)

    edi = aluno(1, 'Edivaldo Ferreira', mensal)
    marina = aluno(2, 'Marina Souza', trimestral)
    carlos = aluno(3, 'Carlos Lima', mensal)
    bianca = aluno(4, 'Bianca Rocha', mensal)
    aluno(5, 'Rafael Costa', mensal, status_cadastro='pendente')
    aluno(6, 'Juliana Alves', trimestral, status_cadastro='pendente')
    aluno(7, 'Thiago Nunes', mensal, ativo=False)

    # Edivaldo: mensalidade do mês anterior paga (vigente) e a do mês seguinte em aberto.
    cobranca(edi, mensal, 'pago', -20, data_pagamento=hoje - timedelta(days=20),
             forma_pagamento='pix', vigencia_inicio=hoje - timedelta(days=20),
             vigencia_fim=hoje + timedelta(days=10))
    cobranca(edi, mensal, 'pendente', 8)
    cobranca(marina, trimestral, 'em_analise', 3, forma_pagamento='comprovante')
    cobranca(carlos, mensal, 'pendente', -12)  # vira "atrasado" sozinho
    cobranca(bianca, mensal, 'pendente', 5)
    # Histórico de receita para os gráficos.
    for meses_atras in (1, 2, 3, 4, 5):
        d = hoje - timedelta(days=30 * meses_atras)
        cobranca(bianca, mensal, 'pago', -30 * meses_atras, data_pagamento=d,
                 forma_pagamento='pix', vigencia_inicio=d, vigencia_fim=d + timedelta(days=30))

    prof = Professor('Anderson Lima', 'prof', 'prof12345')
    db.session.add(prof)
    db.session.commit()
    t1 = Turma('Muay Thai noite', 'Seg,Qua,Sex', '19:00', prof.id, limite_alunos=20)
    t2 = Turma('Jiu-Jitsu manhã', 'Ter,Qui', '07:00', prof.id, limite_alunos=12)
    db.session.add_all([t1, t2])
    db.session.commit()
    for a in (edi, marina, carlos, bianca):
        db.session.add(Matricula(a.id, t1.id))
    db.session.add(Matricula(edi.id, t2.id))
    for n in range(1, 8):
        dia = hoje - timedelta(days=n)
        for a in (edi, marina):
            db.session.add(Presenca(a.id, t1.id, dia, presente=(n % 3 != 0)))
    db.session.commit()

    # --- Casos que costumam quebrar layout ---------------------------------------------
    from datetime import datetime
    from io import BytesIO
    from PIL import Image, ImageDraw
    from servicos.armazenamento import salvar_comprovante_manual

    longo = Plano(nome_plano='Plano Anual Família Premium com Acompanhamento Nutricional',
                  preco_plano=1234.56, duracao_dias=365)
    PlanoDAO.salvar(longo)
    maria = aluno(8, 'Maria Aparecida de Nazaré Albuquerque Cavalcante Figueiredo Neta', longo,
                  email='maria.aparecida.de.nazare.albuquerque.cavalcante@exemplo-de-dominio-muito-longo.com.br',
                  descricao='Alergia a dipirona; lesão antiga no joelho direito; acompanhamento com fisioterapeuta às terças.')
    cobranca(maria, longo, 'pendente', 3)
    aluno(9, 'Aluno Sem Nada', mensal)   # sem cobrança e sem turma: estados vazios

    # Comprovante enviado pela Marina (em análise): habilita o modal de revisão do financeiro.
    img = Image.new('RGB', (600, 800), 'white')
    ImageDraw.Draw(img).text((40, 40), 'COMPROVANTE DE TESTE', fill='black')
    buf = BytesIO()
    img.save(buf, 'PNG')
    pg = Pagamento.query.filter_by(aluno_id=marina.id).first()
    pg.comprovante_manual_arquivo = salvar_comprovante_manual(buf.getvalue())
    pg.comprovante_manual_enviado_em = datetime.utcnow()
    db.session.commit()

print('PRONTO em http://localhost:4002  admin/admin-visual-123  aluno1/senha123  aluno9(vazio)/senha123  prof/prof12345', flush=True)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True
app.run(host='127.0.0.1', port=4002, use_reloader=False, threaded=True)
