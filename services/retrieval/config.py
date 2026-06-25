# central config for the retrieval service
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # qdrant connection
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333

    # collection settings
    COLLECTION_NAME: str = "bows"
    EMBEDDING_DIM: int = 256  # must match model service PROJECTION_DIM
    TOP_K_DEFAULT: int = 3

    class Config:
        env_file = ".env"


config = Config()
