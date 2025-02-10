from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """
    Representa los datos que se envían en la petición para crear un nuevo usuario.
    """
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """
    Representa los datos que se envían en la petición comprobar las credenciales.
    """
    username: str
    password: str

class UserLoginResponse(BaseModel):
    """
    Representa los datos enviados como respuesta de una petición a la api para el login.
    """
    id: int
    username: str
    email: EmailStr
    token: str

class UserResponse(BaseModel):
    """
    Representa los datos enviados como respuesta de una petición a la api.
    """
    id: int
    username: str
    email: EmailStr

    # Es necesario para trabajar con pydantic y SQLAlchemy
    # Esto indica a pydantic que al instanciar la clase se van a usar atributos de la clase modelo en lugar
    # de un diccionario
    class Config:
        from_attributes = True
