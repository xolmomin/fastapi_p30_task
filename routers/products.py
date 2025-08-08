import os

from fastapi import APIRouter

product_router = APIRouter()


@product_router.get('/products')
async def get_products():
    return []
