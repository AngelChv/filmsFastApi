from sqlalchemy import Column, Integer, ForeignKey, Table

from database import Base

list_films_table = Table(
    "list_films", Base.metadata,
    Column("list_id", Integer, ForeignKey("lists.id"), primary_key=True),
    Column("film_id", Integer, ForeignKey("films.id"), primary_key=True)
)
