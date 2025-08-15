from fastapi import APIRouter

from routers.users import user_router
from routers.auth import auth_router
from routers.categories import category_router
from routers.products import product_router

router = APIRouter()
router.include_router(user_router)
router.include_router(category_router)
router.include_router(product_router)
router.include_router(auth_router)
