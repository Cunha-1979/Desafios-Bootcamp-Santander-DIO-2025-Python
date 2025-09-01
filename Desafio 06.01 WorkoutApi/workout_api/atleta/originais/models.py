from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, Integer, String, Float
from workout_api.contrib.models import Basemodel

class AtletaModel(Basemodel):
    __tablename__ = 'atletas'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    cpf: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    idade: Mapped[int] = mapped_column(Integer, nullable=False)
    peso: Mapped[Float] = mapped_column(Float, nullable=False)
    altura: Mapped[Float] = mapped_column(Float, nullable=False)
    sexo: Mapped[str] = mapped_column(String(1), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime, nullable=False)

    # Foreign keys
    categoria_id: Mapped[int] = mapped_column(ForeignKey('categorias.pk_id'))
    centro_treinamento_id: Mapped[int] = mapped_column(ForeignKey('centros_treinamento.pk_id'))

    # Relationships (import local para quebrar ciclo)
    @property
    def categoria(self):
        from workout_api.categorias.models import CategoriaModel
        return relationship(CategoriaModel, back_populates='atletas')

    @property
    def centro_treinamento(self):
        from workout_api.centro_treinamento.models import CentroTreinamentoModel
        return relationship(CentroTreinamentoModel, back_populates='atletas')
