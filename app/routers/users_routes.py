from typing import List

# Importante HTTPException es de fastApi no de HTTP
from fastapi import APIRouter, Depends, HTTPException
# Importante el error es de sqlalchemy no de sqlite3
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session

from app.models.user_model import UserModel
from app.schemas.user_schemas import UserResponse, UserLogin, UserCreate, UserLoginResponse
from app.services import user_service
from database import get_db
from auth import verify_token, oauth2_scheme

router = APIRouter(prefix="/users", tags=["Usuarios"])


@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")

    # Se realiza una consulta y se indica la clase modelo, que representa la tabla de la db.
    # Se recuperan todas las filas.
    users = db.query(UserModel).all()
    return users


@router.post("/login", response_model=UserLoginResponse | None)
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        return user_service.login(user, db)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al iniciar sesión: {str(e)}")


@router.post("/register", response_model=UserLoginResponse | None)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.register(user, db)
    except IntegrityError as e:
        db.rollback()  # Sí hay un error deshacer los cambios.

        # Comprobar el tipo de restricción:
        if "UNIQUE constraint failed" in str(e.orig):
            raise HTTPException(
                status_code=400,
                detail="El nombre de usuario ya existe"
            )

        # Si no es un error manejado devuelvo el error genérico:
        raise HTTPException(status_code=500, detail=f"Error al crear el usuario: {str(e)}")


@router.get("/{username}", response_model=UserResponse | None)
def find_by_username(username: str, db: Session = Depends(get_db)):
    try:
        return user_service.find_by_user_name(username, db)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al obtener el usuario por nombre: {str(e)}")
