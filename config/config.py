from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    """
    配置类
    """
    model_config = SettingsConfigDict(env_file=".env",extra="ignore")

    JWT_SECRET: str
    JWT_ALGORITHM: str
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

Config = Settings()