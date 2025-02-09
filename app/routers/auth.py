# Importante HTTPException es de fastApi no de HTTP
from fastapi import APIRouter, Depends, HTTPException
# Importante el error es de sqlalchemy no de sqlite3
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.user import User
from app.schemas.user import UserResponse, UserCreate
from database import get_db

router = APIRouter(prefix="/auth", tags=["Autenticación"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Encriptar contraseña.
        hashed_password = pwd_context.hash(user.password)
        # Crear usuario modelo.
        db_user = User(username=user.username, email=user.email, password=hashed_password)
        # Insertar en la base de datos.
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback() # Si hay un erro deshacer los cambios.

        # Comprobar el tipo de restricción:
        if "UNIQUE constraint failed" in str(e.orig):
            raise HTTPException(
                status_code = 400,
                detail = "El nombre de usuario ya existe"
            )

        # Si no es un error manejado devuelvo el error genérico:
        raise HTTPException(status_code=500, detail="Error al crear el usuario")
