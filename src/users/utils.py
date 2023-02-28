from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import  OAuth2PasswordBearer
from typing import Optional
from src.users import exceptions
import os

# 시스템에 저장
SECRET_KEY = os.environ.get("JWT_SECRET").__str__()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    """
    plain_password 와 hashed_password 비교
    :param plain_password:
    :param hashed_password:
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
     password를 Bcrypt로 Hash
    :param password:
    :return:
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    사용자 로그인 시 token 생성
    :param data:
    :param expires_delta:
    :return:
    """
    encode_data = data.dict()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    encode_data.update({"exp": expire})
    encoded_jwt = jwt.encode(encode_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user_by_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise exceptions.credential_exception()
    except JWTError:
        raise exceptions.credential_exception()
    return payload



