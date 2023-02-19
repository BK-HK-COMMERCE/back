import uuid

from fastapi import APIRouter, Depends, HTTPException, Body, Query, Path
from sqlalchemy.orm import Session

from database import get_db
from src.products.models import Product
from src.products.schemas import ProductBase, ProductBaseInput

from src.products.service import get_all_products, get_product_by_index_no, add_product, delete_product_by_index_no


router = APIRouter(
    prefix="/products",
    tags=["/products"]
)


@router.get("/", response_model=list[ProductBase])
def all_products(db: Session = Depends(get_db)):
    products = get_all_products(db)
    return products


@router.get("/{index_no}", response_model=ProductBase)
def product_by_index_no(db: Session = Depends(get_db), index_no: int = Path()):
    db_product = get_product_by_index_no(db, index_no)
    if db_product is None:
        raise HTTPException(404, "Product is not found")
    return db_product


@router.post("/")
def create_product(db: Session = Depends(get_db), product_base: ProductBaseInput = Body()):
    db_product = add_product(db, product_base)
    return {"response": db_product}


@router.delete("/{index_no}")
def delete_product(db: Session = Depends(get_db), index_no: int = Query()):
    delete_product_by_index_no(db, index_no)
    return {"response": f"{index_no} Product is deleted"}

