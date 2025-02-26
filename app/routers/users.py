from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestFormStrict
from sqlalchemy import select
from app.schemas import User, UserInfo,Token
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Users, Carts
from sqlalchemy.exc import IntegrityError
from ..security import hash_password, verify_password
from ..auth import create_access_token, verify_access_token
router = APIRouter(
    tags=['Users'],
    prefix='/users'
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

@router.post('/register',status_code=201)
async def register_user(user: User, db: AsyncSession = Depends(get_db)):
    user.password = hash_password(user.password)
    new_user = Users(**user.model_dump())
    try:
        db.add(new_user)
        await db.flush()
        new_cart = Carts(user_id=new_user.id) 
        db.add(new_cart)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    return {"Registered": True, "email": user.email}


@router.post('/login', response_model=Token)
async def login_user(data: dict = Depends(OAuth2PasswordRequestFormStrict), db: AsyncSession = Depends(get_db)):
    email = data.username
    password = data.password
    query = await db.execute(select(Users).filter(Users.email == email)) 
    user_data = query.scalar_one_or_none()
    if not user_data or not verify_password(password, user_data.password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    token_data = {"sub": user_data.email}
    access_token = create_access_token(token_data)

    return {"access_token": access_token, "token_type": "bearer"}
    

@router.get("/me", response_model=UserInfo)
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    user_data = verify_access_token(token)
    
    query = await db.execute(select(Users).filter(Users.email == user_data["sub"]))
    user = query.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user



# @router.get('/{user_id}', response_model=UserInfo)  
# async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
#     user = await db.execute(select(Users).filter(Users.id == user_id))
#     user_data = user.scalar_one_or_none()
#     if not user_data:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user_data

