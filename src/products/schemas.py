from pydantic import BaseModel
from src.products.enums import Size, Category1


class ProductBase(BaseModel):
    uuid: str
    item_name: str
    size: Size
    description: str
    price: float
    category1: Category1
