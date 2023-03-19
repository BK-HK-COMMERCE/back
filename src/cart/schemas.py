from pydantic import BaseModel
from src.products.schemas import ProductBasicInfo

class CartBase(BaseModel):

    user_id: str = None
    product_index: int
    quantity: int = 1
    product: ProductBasicInfo

    class Config:
        orm_mode = True
