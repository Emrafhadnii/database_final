from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    DB_PORT: int
    REDIS_HOST:str
    REDIS_PASS:str
    REDIS_PORT:int
    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_HOST: str
    MONGO_PORT: int
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBIT_URL: str
    GEMINI_API_KEY: str
    GOOGLE_CLOUD_PROJECT: str
    class Config:
        env_file = ".env"

settings = Settings()

