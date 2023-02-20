from fastapi import HTTPException


def product_not_found():
    return HTTPException(404, "Product Not Found")

