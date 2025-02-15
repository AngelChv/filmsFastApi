from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.list_films_model import list_films_table
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
    poster_path = Column(String)

    # Relaciones
    lists = relationship("ListModel", secondary=list_films_table, back_populates="films")
