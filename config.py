from pydantic import BaseSettings


class Config(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY : str

    class Config:
        env_file = '.env'


settings = Config()
