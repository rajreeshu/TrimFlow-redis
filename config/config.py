import os

from pydantic_settings import BaseSettings


class Properties(BaseSettings):
    PORT : int
    REDIS_PORT: int
    PROTOCOL : str
    BASE_URL : str
    COMPLETE_BASE_URL: str
    QUEUE_TIMEOUT : int
    TRIMMED_DIR: str
    UPLOAD_DIR: str
    MAX_WORKERS : int
    CHUNK_SIZE: int
    WIDTH_720P: int
    HEIGHT_720P: int



    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '..', 'environment', f".env.{os.getenv('ENV', 'dev')}")

def ensure_directories_exist(properties1: Properties):
    # os.makedirs(properties.UPLOAD_DIR, exist_ok=True)
    os.makedirs(properties.TRIMMED_DIR, exist_ok=True)

properties = Properties()
ensure_directories_exist(properties)