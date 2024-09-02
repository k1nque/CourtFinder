from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    SECRET: str
    TOKEN: str
    
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )
    
settings = Settings()