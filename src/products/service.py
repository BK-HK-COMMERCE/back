import uuid

from sqlalchemy.orm import Session
from src.products.schemas import ProductBaseInput
from src.products.exceptions import *
from models import Product



def get_all_products(db: Session, page: int):
    """
    전체 Product 조회
    :param db:
    :param page:페이지
    :return:
    """
    search_products = db.query(Product).limit(20).offset(page).all()
    total_products = db.query(Product).count()
    total_pages = (total_products // 20) + 1
    return {
        "list": search_products,
        "total_products": total_products,
        "total_pages": total_pages,
        "current_page": page+1
    }

def get_product_by_index_no(db: Session, index_no: int):
    """
    index_no 로 검색
    :param db:
    :param index_no:
    :return:
    """
    db_product = db.query(Product).filter(Product.index_no == index_no).first()
    if db_product is None:
        raise product_not_found()
    return db_product


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
        raise product_not_found()
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
        raise product_not_found()
    update_data = product_base.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def like_product(db: Session, index_no: int):
    """
    Product Index_no  로 Likes ++
    :param db:
    :param index_no:
    :return:
    """
    # TODO 계정마다 Like 하나마 누를 수 있게 추가
    db_product = db.query(Product).filter(Product.index_no == index_no).first()
    if not db_product:
        raise product_not_found()
    cur_likes = db_product.likes
    db_product.likes = cur_likes + 1
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_by_uuid(db: Session, product_uuid: str) -> Product:
    """
    uuid로 Product 조회
    :param product_uuid:
    :param db:
    :return:
    """
    db_product = db.query(Product).filter(Product.uuid == product_uuid).first()
    if not db_product:
        raise product_not_found()
    return db_product

