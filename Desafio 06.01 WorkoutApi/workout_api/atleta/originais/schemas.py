from typing import Annotated
from pydantic import Field, PositiveFloat
from workout_api.contrib.schemas import BaseSchema, OutMixin


class Atleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do Atleta', example='Joao', max_length=50)]
    cpf: Annotated[int, Field(description='CPF do Atleta somente numeros', example='000.000.000-00', max_length=11)]
    idade: Annotated[int, Field(description='Idade do Atleta', example='28', max_length=2)]
    peso: Annotated[PositiveFloat, Field(description='Peso do Atleta', example='84.50', max_length=4)]
    altura: Annotated[PositiveFloat, Field(description='Altura do Atleta', example='1.84', max_length=3)]
    sexo: Annotated[str, Field(description='Sexo do Atleta', example='M', max_length=1)]
    
class AtletaIn(Atleta):
    pass

class AtletaOut(Atleta, OutMixin):
    pass