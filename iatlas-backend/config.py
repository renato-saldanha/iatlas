from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    #Database
    DATABASE_URL: str
    
    #Security
    SECRET_KEY: str
    
    #API Keys
    GEMIN_API_KEY: str

    #Enviroment
    ENVIROMENT: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()