from sqlalchemy import Column, Integer, String
from database import Base


class FilmModel(Base):
    """
    Definición del modelo de película que va a representar una tabla en la base de datos.
    """
    __tablename__ = "films"

    id = Column(Integer, primary_key=True, index=True) # por defecto es autoincrement
    title = Column(String, nullable=False)
    director = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    poster_path = Column(String, nullable=False)
