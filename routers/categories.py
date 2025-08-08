from fastapi import APIRouter
from pydantic import BaseModel

from database import Category
from schemas.categories import CreateCategory, ReadCategory

categories_router = APIRouter()


@categories_router.get('/category')
async def get_categories():
    return []


@categories_router.post('/category', response_model=ReadCategory)
async def get_categories(data: CreateCategory):
    return await Category.create(**data.model_dump())
