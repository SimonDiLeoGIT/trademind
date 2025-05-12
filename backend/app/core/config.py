# app/core/config.py
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Cargar el archivo .env
load_dotenv()

class Settings(BaseSettings):
    
    TWELVE_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
