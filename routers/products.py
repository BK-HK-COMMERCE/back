from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
from database import get_db

router = APIRouter(
    prefix="/products",
    tags=["/products"]
)



class Image(BaseModel):
    path: str
    image_size: int


@router.get("/")
async def get_all_products(db: Session = Depends(get_db)):
    # TODO User,Admin jwt 추가 예정
    # TODO 검색조건 추가 예정
    products = db.query(models.Product).all()
    dto_list: [Product] = []
    for product in products:
        product_dto = domain_to_dto_product(product)
        images = db.query(models.Image).filter(models.Image.product_id == product.index_no).all()
        for image in images:
            product_dto.img.append(domain_to_dto_image(image))
        dto_list.append(product_dto)
    return {"response": dto_list}


@router.get("/{index_no}")
async def get_product(index_no: int, db: Session = Depends(get_db)):
    # TODO User,Admin jwt 추가 예정
    product = db.query(models.Product).filter(models.Product.index_no == index_no).first()
    if product is None:
        raise http_exception()
    product_dto = domain_to_dto_product(product)

    images = db.query(models.Image).filter(models.Image.product_id == product.index_no).all()

    for image in images:
        product_dto.img.append(domain_to_dto_image(image))

    return product_dto



@router.post("/")
async def create_product(product: Product, db: Session = Depends(get_db)):
    # TODO 관리자 토큰에만 적용 예정
    db_product = models.Product(item_name=product.item_name, \
                                item_code=product.item_code, \
                                size=product.size, \
                                description=product.description, \
                                price=product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    for i in product.img:
        db_image = models.Image(
            path=i.path,
            image_size=i.image_size,
            product_id=db_product.index_no
        )
        db.add(db_image)
        print(db_image)
    print(db_product)
    db.commit()
    return {"response": db_product}


@router.delete("/")
async def delete_product(index_no: int = Body(), db: Session = Depends(get_db)):
    # TODO 관리자 토큰에만 적용 예정
    db_product = db.query(models.Product).filter(models.Product.index_no == index_no).first()
    if db_product is None:
        raise http_exception()
    images = db.query(models.Image).filter(models.Image.product_id == db_product.index_no).all()
    for image in images:
        db.delete(image)
    db.delete(db_product)
    db.commit()
    return f"product {index_no} and images are deleted"


# @router.put("/")
# async def update_product(product: Product, index_no: int, db: Session = Depends(get_db)):
#    # TODO 관리자 토큰에만 적용 예정
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


def domain_to_dto_product(product: models.Product):
    return Product(
        item_name=product.item_name,
        item_code=product.item_code,
        size=product.size,
        description=product.description,
        price=product.price
    )


def domain_to_dto_image(image: models.Image):
    return Image(
        path=image.path,
        image_size=image.image_size
    )

