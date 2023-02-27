from datetime import datetime, timedelta

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt

from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, TOKEN_URL
import schemas , utils

from config import SecuritySettings, TOKEN_URL

settings = SecuritySettings()
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

### hash password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashPassword(pwd: str):
    return pwd_context.hash(pwd)

def verify(input_pwd, hashed_pwd):
    return pwd_context.verify(input_pwd, hashed_pwd)

### OAuth

class OAuth:
    oauth2_schema = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)    
    # expire_time: datetime
    def getExpireTime():
        return {
            "exp" : datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }
    
    def createAccessToken(data: schemas.TokenData):
        expire_time = OAuth.getExpireTime()
        
        return jwt.encode(
            claims = data | expire_time,
            key=SECRET_KEY,
            algorithm=ALGORITHM
        )
    
    def verifyAccessToken(token: str) -> schemas.TokenData:
        try:
            payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError as error:
            raise error
        return schemas.TokenData.parse_obj(payload)


class AuthorizedUser():
    def __init__(self) -> None:
        self.credentials_exception = utils.ForbiddenException(
            msg="Credentials validation fails", 
            headers={"WWW-Authenticate": "Bearer"}
        )
        
        
    def __call__(self, token: str = Depends(OAuth.oauth2_schema)) -> schemas.TokenData:
        try:
            payload = OAuth.verifyAccessToken(token)
            return payload      
        
        except JWTError:
            raise self.credentials_exception
        
    
        