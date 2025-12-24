from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta
from jose import jwt,JWTError
from fastapi import Depends,HTTPException,status
from database import get_db
from user_schema.user_sechema import auth
SCERET_KEY='super-sceret-key'
ALOGRITHM='HS256'
ACCESS_TIME=10
REFRESH_TOKEN_EXPIRE_DAYS = 1
oauth2 = OAuth2PasswordBearer(tokenUrl="/users/login")
pwt_content=CryptContext(schemes=['argon2'],deprecated='auto')


@staticmethod
def hash_password(password:str):
    return pwt_content.hash(password)

@staticmethod
def unhash(password,ver_pass):
    return pwt_content.verify(password,ver_pass)

@staticmethod
def token(data: dict):
    encode_ = data.copy()
    exp = datetime.utcnow() + timedelta(minutes=ACCESS_TIME)
    encode_.update({'exp': exp})
    return jwt.encode(encode_, SCERET_KEY, algorithm=ALOGRITHM)

@staticmethod
def ref_token(data: dict):
    encode_ = data.copy()
    exp = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    encode_.update({'exp': exp})
    return jwt.encode(encode_, SCERET_KEY, algorithm=ALOGRITHM)


def get_current(token:str=Depends(oauth2),db=Depends(get_db)):
    print("TOKEN RECEIVED:", token)
    try:
        payload=jwt.decode(token,SCERET_KEY,algorithms=[ALOGRITHM])
        email=payload.get('sub')
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='email doesnt support')
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='invalid token')
    user=db.query(auth).filter(auth.email==email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    return user