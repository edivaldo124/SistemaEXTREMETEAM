"""Textos editáveis da página inicial: perguntas frequentes e prazos de atendimento.

Edite aqui, não no template. A mesma lista desenha as perguntas na home (<details>) e o
JSON-LD FAQPage lido pelo Google; separar as duas faria o Google mostrar uma resposta
que a página não tem. Texto puro: o template escapa tudo, HTML aqui aparece como texto.
"""

# TODO(revisar): confirmar com a academia o prazo real de resposta no WhatsApp.
TEMPO_RESPOSTA_WHATSAPP = 'em até 1 dia útil'

# TODO(revisar): confirmar com a academia o prazo real de análise do cadastro.
PRAZO_ANALISE_CADASTRO = 'até 2 dias úteis'

# TODO(revisar): revisar cada pergunta e resposta com a academia antes de publicar.
# A última descreve o fluxo que o sistema já faz; as outras são rascunho.
PERGUNTAS_FREQUENTES = [
    {
        'pergunta': 'Posso fazer uma aula experimental antes de contratar?',
        'resposta': (
            'Sim. Fale com a gente pelo WhatsApp para combinar o dia e o horário da sua '
            'aula experimental. Depois dela, é só criar sua conta e escolher o plano.'
        ),
    },
    {
        'pergunta': 'Quais são os horários de treino?',
        'resposta': (
            'Os horários de funcionamento estão na seção de contato, no fim desta página. '
            'Depois que seu cadastro é aprovado, a área do aluno mostra as turmas e os '
            'horários de cada uma.'
        ),
    },
    {
        'pergunta': 'Existe idade mínima para treinar?',
        'resposta': (
            'A idade mínima depende da turma. Fale com a gente pelo WhatsApp para saber '
            'qual turma combina com a idade de quem vai treinar.'
        ),
    },
    {
        'pergunta': 'O que preciso levar no primeiro treino?',
        'resposta': (
            'Roupa confortável para treinar, uma garrafa de água e uma toalha. Se a sua '
            'modalidade pede equipamento próprio, a equipe avisa antes da primeira aula.'
        ),
    },
    {
        'pergunta': 'Como faço o pagamento?',
        'resposta': (
            'Depois que seu cadastro é aprovado, você escolhe o plano na área do aluno e '
            'paga por Pix ou pelas outras formas aceitas pelo Mercado Pago. A mensalidade '
            'fica registrada na sua conta, com o comprovante.'
        ),
    },
]


def faq_estruturado(perguntas):
    """JSON-LD FAQPage com exatamente as perguntas mostradas na página."""
    return {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [
            {
                '@type': 'Question',
                'name': item['pergunta'],
                'acceptedAnswer': {'@type': 'Answer', 'text': item['resposta']},
            }
            for item in perguntas
        ],
    }
