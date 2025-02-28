from fastapi.security import OAuth2PasswordBearer
import jwt
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta, timezone
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Users
from .config import settings


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    print("Token expiration:", expire)  
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired", headers={"WWW-Authenticate": "Bearer"})  
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Couldn't validate the credentials", headers={"WWW-Authenticate": "Bearer"})  


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    user_data = verify_access_token(token)
    
    query = await db.execute(select(Users).filter(Users.email == user_data["sub"]))
    user = query.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def check_role(role):
    def user_role(user: dict = Depends(get_current_user)):
        if role != user.role:
            raise HTTPException(status_code=403, detail="Permissin Denied")
        return user
    return user_role