from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.user_model import UserModel
from app.schemas.user_schemas import UserResponse
from database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    # Se realiza una consulta y se indica la clase modelo, que representa la tabla de la db.
    # Se recuperan todas las filas.
    users = db.query(UserModel).all()
    return users
