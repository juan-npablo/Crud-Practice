from datetime import datetime, timedelta, timezone
from jose import jwt
from jose.exceptions import JWTError
from passlib.context import CryptContext
from .config import Settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def HashPassword(password: str) -> str:
    return pwd_context.hash(password)

def VerifyPassword(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def CreateAccessToken(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
    return encoded_jwt

def DecodeAccessToken(token: str) -> dict:
    try:
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
        return payload
    except JWTError as error:
        raise ValueError("Token inválido: {error}")

