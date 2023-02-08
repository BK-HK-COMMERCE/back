from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from config.database import Base

class Product(Base):
    __tablename__ = "products"

    index_no = Column(Integer, primary_key=True, index=True)
    item_name = Column(String)
    item_code = Column(String, unique=True)
    size = Column(String)
    description = Column(String)
    price = Column(Float)
    img = Column(String)


