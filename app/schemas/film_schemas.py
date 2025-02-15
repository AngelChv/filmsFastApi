from typing import Optional

from pydantic import BaseModel


class FilmCreate(BaseModel):
    """
    Representa los datos que se envían en la petición para crear una nueva película.
    """
    title: str
    director: str
    year: int
    duration: int
    description: str
    poster_path: Optional[str] = None


class FilmUpdate(BaseModel):
    """
    Representa los datos que se envían en la petición para editar una película.
    """
    id: int
    title: str
    director: str
    year: int
    duration: int
    description: str
    poster_path: Optional[str] = None


class FilmResponse(BaseModel):
    """
    Representa los datos enviados como respuesta de una petición a la api
    """
    id: int
    title: str
    director: str
    year: int
    duration: int
    description: str
    poster_path: Optional[str] = None

    # Es necesario para trabajar con pydantic y SQLAlchemy
    # Esto indica a pydantic que al instanciar la clase se van a usar atributos de la clase modelo en lugar
    # de un diccionario
    class Config:
        from_attributes = True
