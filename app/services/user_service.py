from typing import Type

from sqlalchemy.orm import Session

from app.models.user_model import UserModel
from app.schemas.user_schemas import UserCreate, UserLogin


def register(user: UserCreate, db: Session) -> int | None:
    # Crear usuario modelo.
    db_user = UserModel(**user.model_dump())
    # Insertar en la base de datos.
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user.id


def login(user: UserLogin, db: Session) -> Type[UserModel] | None:
    return db.query(UserModel).filter(
        UserModel.username == user.username and UserModel.password == user.password
    ).first()


def find_by_user_name(user_name: str, db: Session) -> Type[UserModel] | None:
    return db.query(UserModel).filter(UserModel.username == user_name).first()
