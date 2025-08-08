from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

from database import Category
from schemas.categories import CreateCategory, ReadCategory, UpdateCategory

category_router = APIRouter()


@category_router.get('/category')
async def get_categories():
    return await Category.get_all()


@category_router.get('/category/{id}')
async def get_category(id: int):
    return await Category.get(id)


@category_router.patch('/category/{id}')
async def get_categories(id: int, data: UpdateCategory):
    await Category.update(id, **data.model_dump(exclude_unset=True))
    return {'message': f'Category {id} updated'}


@category_router.delete('/category/{id}')
async def get_categories(id: int):
    await Category.delete(id)
    return {'message': f'Category {id} deleted'}


@category_router.post('/category', response_model=ReadCategory)
async def get_categories(data: CreateCategory):
    return await Category.create(**data.model_dump())
