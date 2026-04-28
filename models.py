from typing import Optional
from sqlmodel import SQLModel, Field

#MODELO INTEGRANTES
class IntegranteBase(SQLModel):
    nombre: str = Field(min_length=2, max_length=64, description="Nombre del integrante")
    edad: int = Field(gt=0, le=120, description="Edad del integrante")
    altura: float = Field(gt=0.0, le=3.0, description="Altura en metros, ej: 1.78")

class Integrante(IntegranteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


#MODELO ÁLBUM
class AlbumBase(SQLModel):
    nombre: str = Field(min_length=1, max_length=128, description="Nombre del álbum")
    num_canciones: int = Field(gt=0, description="Número de canciones del álbum")


class Album(AlbumBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class AlbumUpdate(SQLModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=128)
    num_canciones: int | None = Field(default=None, gt=0)


#MODELO TOURS
class TourBase(SQLModel):
    nombre: str = Field(min_length=1, max_length=128, description="Nombre del tour")
    ciudades_visitadas: str = Field(
        min_length=1,
        description="Ciudades separadas por coma, ej: 'Seúl, Buenos Aires, Madrid'"
    )


class Tour(TourBase, table=True):
    id: int | None = Field(default=None, primary_key=True)