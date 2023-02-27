
USE_ORM = True
TOKEN_URL = 'login'

from typing import Optional

from pydantic import BaseSettings

class Settings(BaseSettings):
    class Config:
        env_file = ".env"

class DBSettings(Settings):
    DB_URL: Optional[str] = None
    DB_NAME: str
    DB_HOSTNAME: str
    DB_PORT: str
    DB_USERNAME: str
    DB_PWD: str
    
    def getURL(self):
        if self.DB_URL != None:
            return self.DB_URL
        
        # else
        return f"postgresql://{self.DB_USERNAME}:{self.DB_PWD}@{self.DB_HOSTNAME}:{self.DB_PORT}/{self.DB_NAME}"

FASTAPI_TUT_DATABASE_URL = DBSettings().getURL()

class SecuritySettings(Settings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int