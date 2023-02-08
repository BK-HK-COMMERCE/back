from fastapi import FastAPI
from routers import products

import models
from config.database import engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(products.router)