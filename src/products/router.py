import uuid

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from database import get_db
from src.products.models import Product
from src.products.schemas import ProductBase, ProductBaseInput

router = APIRouter(
    prefix="/products",
    tags=["/products"]
)


@router.get("/", response_model=list[ProductBase])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    if products is None:
        raise HTTPException(404, "없음")
    return products


@router.post("/")
def create_product(db: Session = Depends(get_db), product_base: ProductBaseInput = Body()):
    db_product = Product(uuid=uuid.uuid4().__str__(),
                         item_name=product_base.item_name,
                         size=product_base.size,
                         description=product_base.description,
                         price=product_base.price,
                         category1=product_base.category1)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return {"response": db_product}