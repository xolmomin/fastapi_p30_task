from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer, HTTPBearer
from pydantic import BaseModel, Field
from starlette import status
from starlette.responses import JSONResponse

from database import Category, User
from utils.security import create_access_token, verify_password, get_current_user

user_router = APIRouter()


class LoginForm(BaseModel):
    username: str = Field(..., min_length=1, examples=['botir'])
    password: str = Field(..., min_length=1, examples=['123'])


@user_router.post('/login')
async def login_view(data: LoginForm):
    user = await User.get_by_username(data.username)
    if user is None:
        return JSONResponse(
            {'message': 'invalid username or password'},
            status.HTTP_404_NOT_FOUND
        )

    is_valid_password = verify_password(data.password, user.password)
    if not is_valid_password:
        return JSONResponse(
            {'message': 'invalid username or password'},
            status.HTTP_400_BAD_REQUEST
        )
    token = create_access_token({'sub': str(user.id)})
    return JSONResponse(
        {'access_token': token}
    )


@user_router.get('/get-me')
async def get_me_view(current_user: User = Depends(get_current_user)):
    return JSONResponse(
        {'message': f"Current user is {current_user.username}"}
    )


#
# @category_router.post('/category')
# async def get_categories(data: CreateCategory):
#     category = await Category.create(**data.model_dump())
#     return ResponseSchema[ReadCategory](
#         message=f'Category {category.id} created',
#         data=category
#     )
