import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    URL: str
    BUCKET: str
    ACCESS_KEY: str
    SECRET_KEY: str
    REGION: str
    
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.getcwd(), ".env"),
        env_prefix='AWS_',
        extra='ignore',
    )
    
settings = Settings()
