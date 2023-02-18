from sqlalchemy import Column, Integer, String, Enum, Numeric, Text

from database import Base
from src.products.enums import Size, Category1
import uuid


class Product(Base):
    __tablename__ = "PRODUCTS"

    index_no = Column(Integer, primary_key=True)
    uuid = Column(String, default=uuid.uuid4, unique=True, nullable=False)
    item_name = Column(String, nullable=False)
    size = Column(Enum(Size), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    category1 = Column(Enum(Category1), nullable=False)





