import asyncio
import sys
from random import randint

from asgiref.sync import async_to_sync
from celery import Celery

from core.config import settings

celery = Celery(__name__)
celery.conf.broker_url = settings.REDIS_URL
celery.conf.result_backend = settings.REDIS_URL
celery.conf.broker_connection_retry_on_startup = True


async def return_hello():
    await asyncio.sleep(randint(5, 20))
    import os
    sys.path.append(os.getcwd())
    from database import User
    await User.update(1, **{'first_name': 'valijon123'})
    return 'hello'


@celery.task(name='make_order')
def make_order():
    async_to_sync(return_hello)()
    return {'msg': 'finished'}
