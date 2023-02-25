
from pydantic import BaseModel


class ImageBase(BaseModel):
    url: str
    product_index: int
    thumbnail: bool

    class Config:
        orm_mode = True
