import os
from datetime import datetime, timedelta, UTC

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from jwt import encode, decode, ExpiredSignatureError, PyJWTError
from passlib.context import CryptContext

from app.schemas.user_schemas import UserResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "clave_por_defecto")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 120))


def create_access_token(user_response: UserResponse, expires_delta: timedelta | None = None):
    """Genera un token JWT con los datos proporcionados."""
    to_encode = {
        "sub": user_response.username,  # Identificador principal
        "id": user_response.id,
        "username": user_response.username,
        "email": user_response.email
    }
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    """Verifica la validez del token y devuelve su contenido."""
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        # El token ha expirado
        return None
    except PyJWTError:
        # Otro error relacionado con el token
        return None


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


# Test
if __name__ == '__main__':
    # Crear un token
    user = UserResponse(id=1, username="angel", email="angel@gmail.com")
    token_test = create_access_token(user)
    print("Token:", token_test)

    # Verificar un token
    decoded_data = verify_token(token_test)
    print("Decoded data:", decoded_data)
