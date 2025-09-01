from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from workout_api.contrib.models import Basemodel

class CategoriaModel(Basemodel):
    __tablename__ = 'categorias'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)

    @property
    def atletas(self):
        from workout_api.atleta.models import AtletaModel
        return relationship(AtletaModel, back_populates='categoria')
