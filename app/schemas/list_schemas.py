from pydantic import BaseModel


class ListCreate(BaseModel):
    """
    Representa los datos que se envían en la petición para crear una nueva lista.
    """
    name: str
    create_date_time: str
    edit_date_time: str

    class Config:
        # Antes para las relaciones se usaba esto:
        # orm_mode = True
        # Ahora se usa esto.
        from_attributes = True

class ListUpdate(BaseModel):
    """
    Representa los datos que se envían en la petición para editar una lista.
    """
    id: int
    name: str
    create_date_time: str
    edit_date_time: str

    class Config:
        from_attributes = True

class ListResponse(BaseModel):
    """
    Representa los datos enviados como respuesta de una petición a la api
    """
    id: int
    name: str
    create_date_time: str
    edit_date_time: str

    # Es necesario para trabajar con pydantic y SQLAlchemy
    # Esto indica a pydantic que al instanciar la clase se van a usar atributos de la clase modelo en lugar
    # de un diccionario
    class Config:
        from_attributes = True
