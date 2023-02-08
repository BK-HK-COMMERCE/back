from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

import models
from config.database import SessionLocal


router = APIRouter(
    prefix="/products",
    tags=["/products"]
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Product(BaseModel):
    item_name: str
    item_code: str
    size: str
    description: str
    price: float
    img: str



@router.get("/")
async def get_all_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return {"response": products}


@router.get("/{index_no}")
async def get_product(index_no: int, db: Session = Depends(get_db)):
    product = db.query(models.Product)\
        .filter(models.Product.index_no == index_no)\
        .first()
    if product is not None:
        return product
    raise http_exception()


@router.post("/")
async def create_product(product: Product, db: Session = Depends(get_db)):
    db_product = models.Product(item_name=product.item_name,\
                                item_code=product.item_code,\
                                size=product.size,\
                                description=product.description,\
                                price=product.price,\
                                img=product.img)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return {"response": db_product}


@router.delete("/")
async def delete_product(index_no: int = Body(), db: Session = Depends(get_db)):
    db_product = db.query(models.Product.index_no == index_no)
    if db_product is None:
        raise http_exception()
    db.delete(db_product)
    db.commit()
    return f"product {index_no} is deleted"


# @router.put("/")
# async def update_product(product: Product, index_no: int, db: Session = Depends(get_db)):
#     db_product = db.query(models.Product.index_no == index_no).first()
#     if db_product is None:
#         raise http_exception()
#     product_data = product.dict(exclude_unset=True)
#     for key, value in product_data.items():
#         db_product[key] = value
#
#     db.add(db_product)
#     db.commit()
#     db.refresh(db_product)
#     return {"response": {'product': db_product, 'index_no': index_no}}

def http_exception():
    raise HTTPException(status_code=404, detail="PRODUCT NOT FOUND")