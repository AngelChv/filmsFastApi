from sqlalchemy import Column, Integer, String
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
