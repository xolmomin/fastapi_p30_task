from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_HOST: str = Field(default='localhost')
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_DATABASE: str = Field(default='postgres')
    POSTGRES_USER: str = Field(default='postgres')
    POSTGRES_PASSWORD: str = Field(default='1')

    JWT_SECRET_KEY: str = Field(default='secret')
    JWT_ALGORITHM: str = Field(default='HS256')
    JWT_ACCESS_TOKEN_EXPIRE_TIME: int = Field(default=60)
    JWT_REFRESH_TOKEN_EXPIRE_TIME: int = Field(default=3600)

    @property
    def postgres_sync_url(self):
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}"

    @property
    def postgres_async_url(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}"

    class Config:
        env_file = '.env'


settings = Settings()
