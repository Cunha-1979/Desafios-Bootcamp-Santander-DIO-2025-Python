from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from workout_api.contrib.models import Basemodel

class CentroTreinamentoModel(Basemodel):
    __tablename__ = 'centros_treinamento'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    endereco: Mapped[str] = mapped_column(String(60), nullable=False)
    proprietario: Mapped[str] = mapped_column(String(30), nullable=False)

    @property
    def atletas(self):
        from workout_api.atleta.models import AtletaModel
        return relationship(AtletaModel, back_populates='centro_treinamento')
