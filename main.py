from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.base_model import db
from routers import router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await db.create_all()
    print('project ishga tushdi')
    yield
    # await db.drop_all()
    print('project toxtadi')


app = FastAPI(docs_url='/', root_path='/api', title="P30 FastAPI", lifespan=lifespan)

app.include_router(router)
