from celery.result import AsyncResult
from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from core.celery_app import make_order

product_router = APIRouter()


@product_router.post('/make-order')
async def make_order_view():
    task = make_order.delay()

    return ORJSONResponse({
        'message': f'buyurtma qabul qilindi! task id: {task.id}'
    })

@product_router.get('/check-order')
async def make_order_view(task_id):
    result = AsyncResult(task_id)

    return ORJSONResponse({
        'message': f'{result.status}'
    })
