from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.responses import ORJSONResponse
from starlette import status

from database import User
from schemas import RegisterForm
from schemas.auth import LoginPhoneForm
from services.otp_services import OtpService
from utils.utils import generate_code

auth_router = APIRouter()


def otp_service():
    return OtpService()


@auth_router.post('/register')
async def login_view(data: RegisterForm, service: OtpService = Depends(otp_service)):
    user = await User.get_by_username(data['username'])
    if user is not None:
        return ORJSONResponse(
            {'message': 'Username already registered'},
            status.HTTP_400_BAD_REQUEST
        )

    service.save_user_before_registration(data['email'], data)
    code = generate_code()
    print(code)
    service.send_otp_by_email(data['email'], str(code))
    return ORJSONResponse(
        {'message': 'Check your email to verify your account'},
    )


@auth_router.get('/verification-email')
async def login_view(email: str, code: str, service: OtpService = Depends(otp_service)):
    is_verified, user_data = service.verify_email(email, code)
    if is_verified:
        await User.create(**user_data)
        return ORJSONResponse(
            {'message': 'User successfully registered'}
        )
    return ORJSONResponse(
        {'message': 'Invalid or expired code'},
        status.HTTP_400_BAD_REQUEST
    )


@auth_router.post('/login-phone')
async def login_phone_view(data: LoginPhoneForm, service: OtpService = Depends(otp_service)):
    code = generate_code()
    is_sent, _time = service.send_otp_by_phone(data.phone_number, code)
    if not is_sent:
        return ORJSONResponse(
            {'message': f'Smsni {_time} dan keyin yubora olasiz'}
        )
    return ORJSONResponse(
        {'message': 'Sms yuborildi'}
    )
