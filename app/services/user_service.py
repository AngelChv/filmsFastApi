from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user_model import UserModel
from app.schemas.user_schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register(user: UserCreate, db: Session):
    # Encriptar contraseña.
    hashed_password = pwd_context.hash(user.password)
    # Crear usuario modelo.
    db_user = UserModel(username=user.username, email=user.email, password=hashed_password)
    # Insertar en la base de datos.
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
