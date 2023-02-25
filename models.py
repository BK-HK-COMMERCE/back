from sqlalchemy import Column, Integer, String, Enum, Numeric, Text, DATETIME, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from src.products.enums import Size, Category1, Category2, Category3
import uuid


class User(Base):
    __tablename__ = "USERS"

    index_no = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String)
    address = Column(String)
    post_code = Column(String)
    membership_code = Column(String)
    regi_time = Column(DATETIME, nullable=False)
    last_login = Column(DATETIME)



class Product(Base):
    __tablename__ = "PRODUCTS"

    index_no = Column(Integer, primary_key=True)
    uuid = Column(String, default=uuid.uuid4, unique=True, nullable=False)
    item_name = Column(String, nullable=False)
    size = Column(Enum(Size), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    category1 = Column(Enum(Category1), nullable=False)
    category2 = Column(Enum(Category2), nullable=False)
    category3 = Column(Enum(Category3), nullable=False)
    likes = Column(Integer, nullable=False, default=0)

    images = relationship("Image", back_populates="product")


class Image(Base):
    __tablename__ = "IMAGES"

    index_no = Column(Integer, primary_key=True)
    url = Column(String)
    product_index = Column(Integer, ForeignKey("PRODUCTS.index_no"))
    thumbnail = Column(Boolean, default=False, nullable=False)

    product = relationship("Product", back_populates="images")