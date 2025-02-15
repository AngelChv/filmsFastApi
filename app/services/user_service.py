from datetime import timedelta
from typing import Type

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user_model import UserModel
from app.schemas.user_schemas import UserCreate, UserLogin, UserLoginResponse, UserResponse
from auth import create_access_token, hash_password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def register(user: UserCreate, db: Session) -> UserLoginResponse:
    # Encriptar la contraseña
    hashed_password = hash_password(user.password)

    # Crear el nuevo usuario
    db_user = UserModel(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    # Insertar en la base de datos.
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    user_response = UserResponse(id=db_user.id, username=db_user.username, email=db_user.email)

    # Crear el token de acceso
    token = create_access_token(user_response, expires_delta=timedelta(minutes=30))

    # Retornar la respuesta con el token
    return UserLoginResponse(id=db_user.id, username=db_user.username, email=db_user.email, token=token)


def login(user: UserLogin, db: Session) -> UserLoginResponse | None:
    # todo: necesito que la contraseña no esté encriptada.
    # Buscar usuario
    db_user = find_by_user_name(user.username, db)

    # Verificar que el usuario existe y la contraseña es correcta
    if not db_user or not verify_password(user.password, db_user.password):
        return None # Usuario no encontrado o contraseña incorrecta

    user_response = UserResponse(id=db_user.id, username=db_user.username, email=db_user.email)

    # Crear token
    token = create_access_token(user_response, expires_delta=timedelta(minutes=30))

    # Devolver usuario con el token:
    return UserLoginResponse(id=db_user.id, username=db_user.username, email=db_user.email, token=token)


def find_by_user_name(user_name: str, db: Session) -> Type[UserModel] | None:
    return db.query(UserModel).filter(UserModel.username == user_name).first()
