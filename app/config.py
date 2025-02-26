from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST : str
    DB_USER : str
    DB_PASSWORD : str
    DB_NAME : str
    DB_PORT : int
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file= ".env"
 
settings = Settings()