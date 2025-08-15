from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    msg = exc.args[0][0]['msg']
    return JSONResponse(
        {'message': msg},
        status.HTTP_400_BAD_REQUEST,
    )


app.include_router(router)
