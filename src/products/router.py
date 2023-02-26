import uuid

from fastapi import APIRouter, Depends, HTTPException, Body, Query, Path, Form
from sqlalchemy.orm import Session

from database import get_db
from src.products import service, schemas


router = APIRouter(
    prefix="/products",
    tags=["products"]
)


@router.get("/")
def all_products(db: Session = Depends(get_db),
                 page: int = Query(default=0, ge=0)):
    products = service.get_all_products(db, page)
    return products


@router.get("/{index_no}", response_model=schemas.ProductBase)
def product_by_index_no(db: Session = Depends(get_db), index_no: int = Path()):
    db_product = service.get_product_by_index_no(db, index_no)
    if db_product is None:
        raise HTTPException(404, "Product is not found")
    return db_product


@router.post("/")
def create_product(db: Session = Depends(get_db), product_base: schemas.ProductBaseInput = Body()):
    db_product = service.add_product(db, product_base)
    return {"response": db_product}


@router.delete("/{index_no}")
def delete_product(db: Session = Depends(get_db), index_no: int = Path()):
    service.delete_product_by_index_no(db, index_no)
    return {"response": f"{index_no} Product is deleted"}


@router.put("/{index_no}")
def update_product(db: Session = Depends(get_db),
                   index_no: int = Path(),
                   product_base: schemas.ProductBaseInput = Body()):
    updated_product: schemas.ProductBase = service.update_product_by_index_no(db, index_no, product_base)

    return {
        "response": f"{index_no} Product is updated",
        "updated_product": updated_product
    }


@router.put("/like/{index_no}")
def like_product(db: Session = Depends(get_db),
                 index_no: int = Path()):
    db_product = service.like_product(db, index_no)
    return {
        "response": f"{db_product.item_name}'s like : {db_product.likes}"
    }


