from fastapi import APIRouter

from routers.categories import categories_router
from routers.products import product_router

router = APIRouter()
router.include_router(categories_router)
router.include_router(product_router)
