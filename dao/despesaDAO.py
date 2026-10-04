from config import db
from modelos.despesa import Despesa


class DespesaDAO:
    @staticmethod
    def salvar(despesa):
        db.session.add(despesa)
        db.session.commit()

    @staticmethod
    def buscar_por_id(despesa_id):
        return db.session.get(Despesa, despesa_id)

    @staticmethod
    def excluir(despesa):
        db.session.delete(despesa)
        db.session.commit()

    @staticmethod
    def listar_periodo(inicio, fim):
        """Saídas com data em [inicio, fim], da mais recente para a mais antiga."""
        return (
            Despesa.query
            .filter(Despesa.data >= inicio, Despesa.data <= fim)
            .order_by(Despesa.data.desc(), Despesa.id.desc())
            .all()
        )
