from fastapi import APIRouter

from routers.categories import category_router
from routers.products import product_router

router = APIRouter()
router.include_router(category_router)
router.include_router(product_router)
