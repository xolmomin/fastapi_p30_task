from orjson import orjson
from redis import Redis

from core.config import settings
from utils.utils import verification_send_email


class OtpService:
    def __init__(self):
        self.redis_client = Redis.from_url(settings.REDIS_URL)

    def _get_otp_phone_key(self, phone: str) -> str:
        return f"send_otp_phone:{phone}"

    def _get_otp_email_key(self, phone: str) -> str:
        return f"send_otp_email:{phone}"

    def _get_registration_key(self, email: str) -> str:
        return f"registration:{email}"

    def send_otp_by_phone(self, phone: str, code: int, expire_time=60) -> tuple[bool, int]:
        _key = self._get_otp_phone_key(phone)
        _ttl = self.redis_client.ttl(_key)
        if _ttl > 0:
            return False, _ttl
        self.redis_client.set(_key, code, expire_time)
        return True, 0

    def send_otp_by_email(self, email: str, code: str, expire_time=60) -> tuple[bool, int]:
        _key = self._get_otp_email_key(email)
        # _ttl = self.redis_client.ttl(_key)
        # if _ttl > 0:
        #     return False, _ttl
        self.redis_client.set(_key, code, expire_time)

        verification_send_email(email, code)
        return True, 0

    def save_user_before_registration(self, email: str, user_data: dict, expire_time=120):
        _key = self._get_registration_key(email)
        _ttl = self.redis_client.ttl(_key)
        if _ttl > 0:
            return False, _ttl
        user_data = orjson.dumps(user_data)
        self.redis_client.set(_key, user_data, expire_time)
        return True, 0

    def verify_email(self, email: str, code: str) -> tuple[bool, dict]:
        saved_code = self.redis_client.get(self._get_otp_email_key(email))
        user_data = self.redis_client.get(self._get_registration_key(email))
        if saved_code:
            saved_code = saved_code.decode()

        user_data = orjson.loads(user_data)
        return saved_code == code, user_data
