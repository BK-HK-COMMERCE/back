import uuid

from sqlalchemy.orm import Session
from src.products.models import Product
from src.products.schemas import ProductBaseInput
from fastapi import HTTPException



def get_all_products(db: Session):
    """
    전체 Product 조회
    :param db:
    :return:
    """
    return db.query(Product).all()


def get_product_by_index_no(db: Session, index_no: int):
    """
    index_no 로 검색
    :param db:
    :param index_no:
    :return:
    """
    return db.query(Product).filter(Product.index_no == index_no).first()


def add_product(db: Session, product_base: ProductBaseInput):
    """
    Product 등록
    :param db:
    :param product_base:
    :return:
    """
    db_product = Product(
        uuid=uuid.uuid4().__str__(),
        item_name=product_base.item_name,
        size=product_base.size,
        description=product_base.description,
        price=product_base.price,
        category1=product_base.category1,
        category2=product_base.category2,
        category3=product_base.category3,
        likes=0
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


def delete_product_by_index_no(db: Session, index_no: int):
    """
    index_no 로 Product 삭제
    :param db:
    :param index_no:
    :return:
    """
    db_product = db.query(Product).filter(Product.index_no == index_no).first()
    if db_product is None:
        raise HTTPException(404, "Product is not found")

    db.delete(db_product)
    db.commit()


def update_product_by_index_no(db: Session, index_no: int, product_base: ProductBaseInput):
    """
    Product 업데이트
    :param db:
    :param index_no:
    :param product_base:
    :return:
    """
    db_product = db.query(Product).filter(Product.index_no == index_no).first()
    if db_product is None:
        raise HTTPException(404, "Product is not found")
    update_data = product_base.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product






