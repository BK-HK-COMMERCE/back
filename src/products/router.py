import uuid

from fastapi import APIRouter, Depends, HTTPException, Body, Query
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


@router.delete("/{index_no}")
def delete_product(db: Session = Depends(get_db), index_no: int = Query()):
    db_product = db.query(Product).filter(Product.index_no == index_no).first()
    if db_product is None:
        raise HTTPException(404, "Product is not found")

    db.delete(db_product)
    db.commit()
    return {"response": f"{index_no} Product is deleted"}

