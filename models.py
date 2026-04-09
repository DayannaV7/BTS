from pydantic import BaseModel, Field
from pokemon_types import PokemonType
from typing import Optional


class PokemonBase(BaseModel):
    name: str = (Field
                 (...,
                  min_length=3,
                  max_length=64))
    type: PokemonType = Field(...
                              )
    level: int = Field(...,
                       gt=0,
                       le=100)


class PokemonID(PokemonBase):
    id: int = Field(..., gt=0)
