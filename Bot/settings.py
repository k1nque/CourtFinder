from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TOKEN: str
    
    MONGO_HOST: str
    MONGO_PORT: str
    # MONGO_USERNAME: str
    # MONGO_PASSWORD: str
    
    API_HOST: str
    API_PORT: str
    
    def get_connection_string(self) -> str:
        # return f"mongodb://{self.MONGO_USERNAME}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}"
        return f"mongodb://{self.MONGO_HOST}:{self.MONGO_PORT}"
    
    def get_api_url(self) -> str:
        return f"http://{self.API_HOST}:{self.API_PORT}/"
    
    
settings = Settings()