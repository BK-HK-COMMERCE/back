from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.products.router import router as products_router
from src.users.router import router as users_router
from src.auth.router import router as auth_router
from database import Base, engine
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(products_router)
app.include_router(users_router)
app.include_router(auth_router)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
