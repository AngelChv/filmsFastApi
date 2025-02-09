# Importante HTTPException es de fastApi no de HTTP
from fastapi import APIRouter, Depends, HTTPException
# Importante el error es de sqlalchemy no de sqlite3
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.schemas.user_schemas import UserResponse, UserCreate
from app.services import user_service
from database import get_db

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.register(user, db)
    except IntegrityError as e:
        db.rollback() # Si hay un erro deshacer los cambios.

        # Comprobar el tipo de restricción:
        if "UNIQUE constraint failed" in str(e.orig):
            raise HTTPException(
                status_code = 400,
                detail = "El nombre de usuario ya existe"
            )

        # Si no es un error manejado devuelvo el error genérico:
        raise HTTPException(status_code=500, detail=f"Error al crear el usuario: {str(e)}")
