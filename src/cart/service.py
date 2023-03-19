
from sqlalchemy.orm import Session, joinedload
from fastapi import Cookie, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.users.utils import get_current_user_by_token
from models import Cart
from src.products import service as products_service
import json


def get_carts(db: Session, token: str, request: Request):
    if token:
        # 토큰 정보로 Cart조회
        payload = get_current_user_by_token(token)
        user_id: str = payload.get("user_id")
        carts: list = get_carts_by_user_id(db, user_id)
        return carts
    else:
        # TODO 쿠키로 조회
        cookie_carts = get_carts_cookie(request)
        if cookie_carts:
            carts: list[dict] = json.loads(cookie_carts.replace("'", "\""))
            for cart in carts:
                uuid = cart.get("uuid")
                if uuid:
                    product = products_service.get_by_uuid(db, uuid)
                    if product:
                        cart["product_index"] = product.index_no
                        cart["product"] = product
            return carts
        else:
            return []


def get_carts_by_user_id(db: Session, user_id: str):
    return db.query(Cart).options(joinedload(Cart.product)).filter(Cart.user_id == user_id).all()


def get_carts_cookie(request: Request) -> str:
    """
    carts 쿠키 조회
    :param request: 
    :return: 
    """
    cookie_value = request.cookies.get("carts")
    return cookie_value


def add_item_to_cart(db: Session,
                     request: Request,
                     response: Response,
                     token: str,
                     uuid: str):
    """
    Cart 추가 ,
    비회원 - 쿠키
    회원 - Cart 테이블 저장
    :param db: 
    :param request: 
    :param response: 
    :param token: 
    :param uuid: 
    :return: 
    """
    if not uuid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No item uuid")
    if token:
        try:
            payload = get_current_user_by_token(token)
            user_id: str = payload.get("user_id")
        except:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
        db_product = products_service.get_by_uuid(db, uuid)
        if not db_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        carts: list[Cart] = get_carts_by_user_id(db, user_id)
        old_product_id = [cart.index_no for cart in carts]
        if db_product.index_no not in old_product_id:
            new_cart: Cart = Cart(user_id=user_id, product_index=db_product.index_no, quantity=1)
            db.add(new_cart)
            db.commit()
            carts = get_carts_by_user_id(db, user_id)
        return carts
    else:
        cookie_carts = get_carts_cookie(request)
        if cookie_carts:
            carts: list[dict] = json.loads(cookie_carts.replace("'", "\""))
            product_list: list = [cart["uuid"] for cart in carts]
            if uuid not in product_list:
                carts.append({
                    "uuid": uuid,
                    "quantity": 1
                })
            response.set_cookie(key="carts", value=jsonable_encoder(carts))
            return carts
        else:
            carts: list[dict] = [{
                "uuid": uuid,
                "quantity": 1
            }]
            response.set_cookie(key="carts", value=jsonable_encoder(carts))
            return carts
