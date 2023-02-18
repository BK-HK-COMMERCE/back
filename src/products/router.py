from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from src.products.models import Product
from src.products.schemas import ProductBase

router = APIRouter(
    prefix="/products",
    tags=["/products"]
)


@router.get("/", response_model=dict[str, list[ProductBase]])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    if products is None:
        raise HTTPException(404, "없음")
    return {"response": products}
