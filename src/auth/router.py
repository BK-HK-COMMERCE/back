from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from database import get_db
from src.users import service as user_service, schemas as user_schemas

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login")
def login(db: Session = Depends(get_db), login_input: user_schemas.LoginInput = Body()):
    token = user_service.login(db, login_input)
    return {"token": token}


