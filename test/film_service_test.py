import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.schemas.film_schemas import FilmCreate
from app.services import film_service

from database import Base

# Aunque a veces aparezca como que no se usan los imports, son completamente necesarios para que funcione
# la creación de la base de datos en memoria con: Base.metadata.create_all()
from app.models.film_model import FilmModel
from app.models.list_model import ListModel
from app.models.user_model import UserModel
from app.models.list_films_model import list_films_table

# Configurar base de datos de prueba en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Crea una sesión de prueba con una base de datos en memoria"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Borrar la base de datos después de los tests.
        Base.metadata.drop_all(bind=engine)


def test_create_film(db_session):
    """Prueba la creación de una película"""
    new_film = FilmCreate(
        title="Interstellar",
        director="Christopher Nolan",
        year=2014,
        duration=169,
        description="Ciencia ficción sobre viajes espaciales.",
        poster_path="/path/to/poster.jpg"
    )

    film_id = film_service.create_film(new_film, db_session)
    assert film_id is not None

    film = db_session.query(FilmModel).filter(FilmModel.id == film_id).first()
    assert film is not None
    assert film.title == "Interstellar"


def test_get_films(db_session):
    """Prueba obtener películas desde la base de datos"""
    film1 = FilmModel(title="Inception", director="Christopher Nolan", year=2010, duration=148,
                      description="Sueños dentro de sueños.", poster_path="/path/inception.jpg")
    film2 = FilmModel(title="The Matrix", director="Wachowski", year=1999, duration=136,
                      description="Simulación y realidad.", poster_path="/path/matrix.jpg")

    db_session.add(film1)
    db_session.add(film2)
    db_session.commit()

    films = film_service.get_films(db_session)
    assert len(films) == 2
    assert films[0].title == "Inception"
    assert films[1].title == "The Matrix"


if __name__ == "__main__":
    pytest.main(["-v", "--tb=short"])
