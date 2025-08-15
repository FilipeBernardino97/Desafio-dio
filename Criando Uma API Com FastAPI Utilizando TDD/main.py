main.py

from fastapi import FastAPI
from src.controllers.product import product_router

app = FastAPI(title="Store API")

@app.get("/")
def home():
    return {"message": "Hello, World!"}

app.include_router(product_router)