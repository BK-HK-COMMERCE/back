from fastapi import APIRouter, Depends, Query, Request, Body, Response
from sqlalchemy.orm import Session
from database import get_db
from src.cart import service, schemas
router = APIRouter(
    prefix="/carts",
    tags=["carts"]
)


@router.get("/",response_model=list[schemas.CartBase])
def get_carts(db: Session = Depends(get_db),
              token: str = Query(default=None),
              request: Request = Request):
    carts = service.get_carts(db, token, request)
    return carts


@router.post("/")
def add_to_cart(db: Session = Depends(get_db),
                request: Request = Request,
                response: Response = Response,
                token: str = Body(default=None),
                uuid: str = Body()):
    carts = service.add_item_to_cart(db, request, response, token, uuid)
    return {
        "carts": carts
    }
