from fastapi import FastAPI
from src.products.router import router as products_router
from database import Base, engine
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(products_router)

