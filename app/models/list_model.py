from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.list_films_model import list_films_table
from database import Base


class ListModel(Base):
    """
    Definición del modelo de una lista que va a representar una tabla en la base de datos.
    """
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, index=True) # por defecto es autoincrement
    name = Column(String, nullable=False)
    create_date_time = Column(String, nullable=False)
    edit_date_time = Column(String, nullable=False)

    # Relaciones
    # Representa la columna de la base de datos para la clave foránea.
    # En la ForeignKey hay que indicar la columna de la base de datos con la que se relaciona, importante poner
    # el mismo nombre de tabla que el indicado en el modelo. En este caso users en minúscula y plural.
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Representa un objeto de la clase indicada, en este caso UserModel, que construye la relación.
    # back_populates indica que la relación es bidireccional y, por lo tanto, debe de haber un atributo lists.
    user = relationship("UserModel", back_populates="lists")  # Relación con el modelo de usuario
    films = relationship("FilmModel", secondary=list_films_table, back_populates="lists")

