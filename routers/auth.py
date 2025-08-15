from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.responses import ORJSONResponse
from starlette import status
from database import User
from schemas import RegisterForm
from schemas.auth import LoginPhoneForm
from services.otp_services import OtpService
from utils.security import create_access_token, verify_password, get_current_user
from utils.utils import generate_code

auth_router = APIRouter()


def otp_service():
    return OtpService()


@auth_router.post('/register')
async def login_view(data: RegisterForm):
    user = await User.get_by_username(data['username'])
    if user is not None:
        return ORJSONResponse(
            {'message': 'Username already registered'},
            status.HTTP_400_BAD_REQUEST
        )
    await User.create(**data)
    return ORJSONResponse(
        {'message': 'User registered'}
    )


@auth_router.post('/login-phone')
async def login_phone_view(data: LoginPhoneForm, service: OtpService = Depends(otp_service)):
    code = generate_code()
    is_sent, _time = service.send_otp(data.phone_number, code)
    if not is_sent:
        return ORJSONResponse(
            {'message': f'Smsni {_time} dan keyin yubora olasiz'}
        )
    return ORJSONResponse(
        {'message': 'Sms yuborildi'}
    )
