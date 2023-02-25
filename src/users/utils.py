from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

from typing import Optional

# TODO 배포 후 시스템에 저장하여 가져올 예정
SECRET_KEY = "c158f095ebd97a6aa72f82cee96981b61b99d69e2404f8217ca6525a59506c52"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
    token 생성
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



