from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.token_schemas import Token
from app.schemas.user_schemas import UserLogin
from app.services.user_service import find_by_user_name, verify_password
from auth import create_access_token
from database import get_db

router = APIRouter(prefix="/token", tags=["Token"])

@router.post("/", response_model=Token)
def get_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Buscar usuario
    user_login = UserLogin(username=form_data.username, password=form_data.password)
    db_user = find_by_user_name(user_login.username, db)

    # Verificar que el usuario existe y la contraseña es correcta
    if not db_user or not verify_password(form_data.password, db_user.password):
        return None # Usuario no encontrado o contraseña incorrecta

    # Crear token
    token = create_access_token(data={"sub": db_user.username}, expires_delta=timedelta(minutes=30))

    # Devolver el token
    return Token(access_token=token, token_type="Bearer")
