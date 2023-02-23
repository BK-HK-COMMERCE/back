from sqlalchemy.orm import Session
from models import User
from src.users import schemas, utils, exceptions

import datetime


def get_all_users(db: Session):
    """
    전체 User 조회
    :param db:
    :return:
    """
    return db.query(User).all()


def add_user(db: Session, user_base: schemas.UserBaseInput):
    """
    User 등록
    :param db:
    :param user_base:
    :return:
    """
    db_user = User(
        user_id=user_base.user_id,
        password=utils.get_password_hash(user_base.password),
        name=user_base.name,
        email=user_base.email,
        phone=user_base.phone,
        address=user_base.address,
        post_code=user_base.post_code,
        regi_time=datetime.datetime.now()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user(db: Session, user_id: str):
    """
    user_id 로 User 조회
    :param db:
    :param user_id:
    :return:
    """
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise exceptions.user_not_found()
    return db_user

