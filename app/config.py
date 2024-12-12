from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    database_username: str
    database_name: str
    database_password: str
    database_port: str
    database_host: str
    secret_key: str
    algorithm: str
    expiry_time_taken: int

#     model_config = SettingsConfigDict(env_file=".env")


# settings = Settings()
settings = Settings(
    database_username=os.getenv("DATABASE_USERNAME"),
    database_name=os.getenv("DATABASE_NAME"),
    database_password=os.getenv("DATABASE_PASSWORD"),
    database_port=os.getenv("DATABASE_PORT"),
    database_host=os.getenv("DATABASE_HOST"),
    secret_key=os.getenv("SECRET_KEY"),
    algorithm=os.getenv("ALGORITHM"),
    expiry_time_taken=int(os.getenv("EXPIRY_TIME_TAKEN"))
)
