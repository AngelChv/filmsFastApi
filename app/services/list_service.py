from sqlalchemy.orm import Session

from app.models.list_model import ListModel
from app.models.user_model import UserModel
from app.schemas.list_schemas import ListCreate, ListUpdate
from app.services import film_service


def find_by_id(list_id: int, db: Session):
    return db.query(ListModel).filter(ListModel.id == list_id).first()


def find_all_by_user_id(user_id: int, db: Session):
    return db.query(ListModel).filter(ListModel.user_id == user_id).all()


def create_list(list_create: ListCreate, db: Session):
    db_list = ListModel(**list_create.model_dump())
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list.id


def update_list(list_update: ListUpdate, db: Session):
    db_list = find_by_id(list_update.id, db)
    if db_list:
        # Editar lista
        db_list.name = list_update.name
        db_list.create_date_time = list_update.create_date_time
        db_list.edit_date_time = list_update.edit_date_time

        # Guardar cambios
        db.commit()
        db.refresh(db_list)

    return db_list


def delete_list(list_id: int, db: Session):
    db_list = find_by_id(list_id, db)
    if db_list:
        # Eliminar película
        db.delete(db_list)
        db.commit()
        return True

    return False

def add_film_to_list(list_id: int, film_id: int, db: Session):
    db_list = find_by_id(list_id, db)
    db_film = film_service.find_by_id(film_id, db)
    if db_list and db_film:
        db_list.films.append(db_film)
        db.commit()
        return True
    return False

def remove_film_from_list(list_id: int, film_id: int, db: Session):
    db_list = find_by_id(list_id, db)
    db_film = film_service.find_by_id(film_id, db)
    if db_list and db_film and db_film in db_list.films:
        db_list.films.remove(db_film)
        db.commit()
        return True
    return False

def count_all_of_user(user_id: int, db: Session) -> int:
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user:
        return len(db_user.lists)
    return 0