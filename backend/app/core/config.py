# app/core/config.py
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Cargar el archivo .env
load_dotenv()

class Settings(BaseSettings):
    
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    TWELVE_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
