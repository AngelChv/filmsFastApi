from typing import List

# Importante HTTPException es de fastApi no de HTTP
from fastapi import APIRouter, Depends, HTTPException
# Importante el error es de sqlalchemy no de sqlite3
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session

from app.models.user_model import UserModel
from app.schemas.user_schemas import UserResponse, UserLogin, UserCreate
from app.services import user_service
from database import get_db

router = APIRouter(prefix="/users", tags=["Usuarios"])

@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    # Se realiza una consulta y se indica la clase modelo, que representa la tabla de la db.
    # Se recuperan todas las filas.
    users = db.query(UserModel).all()
    return users


@router.post("/login", response_model=UserResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        return user_service.login(user, db)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al iniciar sesión: {str(e)}")


@router.post("/register", response_model=int | None)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.register(user, db)
    except IntegrityError as e:
        db.rollback()  # Si hay un erro deshacer los cambios.

        # Comprobar el tipo de restricción:
        if "UNIQUE constraint failed" in str(e.orig):
            raise HTTPException(
                status_code=400,
                detail="El nombre de usuario ya existe"
            )

        # Si no es un error manejado devuelvo el error genérico:
        raise HTTPException(status_code=500, detail=f"Error al crear el usuario: {str(e)}")
