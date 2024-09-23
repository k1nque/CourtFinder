from json import loads
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    SECRET: str
    TOKEN: str
    
    model_config = SettingsConfigDict(
        extra="allow",
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )
    
    def __init__(self):
        super().__init__(**self.model_config)
        with open("ArbitrationCourts.json", "r") as f:
            self.ARBITRATION_COURTS = loads(f.read())

    
settings = Settings()