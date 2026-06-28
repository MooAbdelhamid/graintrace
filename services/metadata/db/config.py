from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DB_HOST: str = "localhost"
    DB_NAME: str = "Metadata"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "123Mm123"

    class Config:
        env_file = ".env"


config = Config()


def get_connection_string(database=None):

    return {
        "host": config.DB_HOST,
        "port": config.DB_PORT,
        "user": config.DB_USER,
        "password": config.DB_PASSWORD,
        "database": database or "postgres",
    }
