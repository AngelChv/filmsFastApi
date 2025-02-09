from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class UserModel(Base):
    """
    Definición del modelo de usuario que va a representar una tabla en la base de datos.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    # Relaciones
    # El primer argumento significa el modelo con el que se representa la relación.
    # El segundo argumento representa el atributo de la otra clase que indica la relación
    # El tercer argumento indica que si se elimina un usuario se eliminan todas las listas asociadas.
    lists = relationship("ListModel", back_populates="user", cascade="all, delete-orphan")