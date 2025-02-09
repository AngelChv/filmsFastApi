from sqlalchemy.orm import Session

from app.models.film_model import FilmModel
from app.schemas.film_schemas import FilmCreate, FilmUpdate


def get_films(db: Session):
    return db.query(FilmModel).all()


def find_by_id(film_id: int, db: Session):
    return db.query(FilmModel).filter(FilmModel.id == film_id).first()


def create_film(film: FilmCreate, db: Session):
    db_film = FilmModel(**film.model_dump())
    db.add(db_film)
    db.commit()
    db.refresh(db_film)
    return db_film.id


def update_film(film: FilmUpdate, db: Session):
    db_film = find_by_id(film.id, db)
    if db_film:
        # Editar película
        db_film.title = film.title
        db_film.director = film.director
        db_film.year = film.year
        db_film.duration = film.duration
        db_film.description = film.description
        db_film.poster_path = film.poster_path

        # Guardar cambios
        db.commit()
        db.refresh(db_film)

    return db_film


def delete_film(film_id: int, db: Session):
    db_user = find_by_id(film_id, db)
    if db_user:
        # Eliminar película
        db.delete(db_user)
        db.commit()
        return True

    return False


def count(db: Session):
    return db.query(FilmModel).count()
