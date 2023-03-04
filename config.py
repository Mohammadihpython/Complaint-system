from pydantic import BaseSettings


class Config(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

    AWS_ACCESS_KEY: str
    AWS_SECRET: str
    AWS_REGION: str
    AWS_BUCKET_NAME: str
    LOCALSTACK_URL : str

    class Config:
        env_file = '.env'


settings = Config()
