import os

from fastapi import APIRouter

from schemas import CreateProduct

product_router = APIRouter()

# @product_router.get('/products')
# async def get_products():
#     return []
