from redis import Redis

from core.config import settings


class OtpService:
    def __init__(self):
        self.redis_client = Redis.from_url(settings.REDIS_URL)

    def _get_otp_key(self, phone: str) -> str:
        return f"send_otp:{phone}"

    def send_otp(self, phone: str, code: int, expire_time=60) -> tuple[bool, int]:
        _key = self._get_otp_key(phone)
        _ttl = self.redis_client.ttl(_key)
        if _ttl > 0:
            return False, _ttl
        self.redis_client.set(_key, code, expire_time)
        return True, 0
