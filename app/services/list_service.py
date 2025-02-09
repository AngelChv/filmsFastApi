from sqlalchemy.orm import Session

from app.models.film_model import FilmModel
from app.models.list_model import ListModel
from app.schemas.film_schemas import FilmCreate, FilmUpdate
from app.schemas.list_schemas import ListCreate, ListUpdate


def find_by_id(list_id: int, db: Session):
    return db.query(ListModel).filter(ListModel.id == list_id).first()


def find_all_by_user_id(user_id: int, db: Session):
    return db.query(ListModel).filter(ListModel.user_id == user_id).all()


def create_list(list_create: ListCreate, user_id: int, db: Session):
    db_list = ListModel(**list_create.model_dump())
    db_list.user_id = user_id
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
