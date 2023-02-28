from sqlalchemy.orm import Session
from models import User
from src.users import schemas, utils, exceptions
from fastapi.encoders import jsonable_encoder
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


def login(db: Session, login_input: schemas.LoginInput):
    """
    로그인 후 토큰 전달
    :param db:
    :param login_input:
    :return:
    """
    db_user: User = db.query(User).filter(User.user_id == login_input.user_id).first()
    if not db_user:
        raise exceptions.login_fail()

    if not utils.verify_password(login_input.password, db_user.password):
        raise exceptions.login_fail()

    data: schemas.Token = jsonable_encoder(db_user, exclude_unset=True)

    token = schemas.Token(**data)

    # token으로 변경
    return utils.create_access_token(token, None)


def get_current_user(db: Session, token: str):
    """
    토큰 전송하여 현재 사용자 불러오기
    :param db:
    :param token:
    :return:
    """
    payload = utils.get_current_user_by_token(token)
    return get_user(db, payload.get("user_id"))

