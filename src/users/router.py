from fastapi import APIRouter, Depends, Body, Path
from sqlalchemy.orm import Session

from database import get_db
from src.users import service, schemas
router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/", response_model=list[schemas.UserBase])
def get_all_users(db: Session = Depends(get_db)):
    users = service.get_all_users(db)
    return users


@router.get("/{user_id}", response_model=schemas.UserBase)
def get_user(db: Session = Depends(get_db), user_id: str = Path()):
    user = service.get_user(db, user_id)
    return user


@router.post("/")
def create_user(db: Session = Depends(get_db), user_base: schemas.UserBaseInput = Body()):
    db_user = service.add_user(db, user_base)
    return {"response": db_user}


@router.post("/login")
def login(db: Session = Depends(get_db), login_input: schemas.LoginInput = Body()):
    token = service.login(db, login_input)
    return {"token": token}



