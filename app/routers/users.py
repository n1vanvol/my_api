from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select, insert
from app.schemas import User, UserInfo
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Users, Carts
from sqlalchemy.exc import IntegrityError
router = APIRouter(
    tags=['Users'],
    prefix='/users'
)


@router.post('/register',status_code=201)
async def register_user(user: User, db: AsyncSession = Depends(get_db)):
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


@router.post('/login',status_code=200)
async def login_user(user: User, db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(Users).filter(Users.email == user.email, Users.password == user.password))
    user_data = query.scalar_one_or_none()
    if user_data:
        return {"Authorized": True}
    raise HTTPException(status_code=401, detail="Invalid Credentials")


@router.get('/{user_id}', response_model=UserInfo)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(Users).filter(Users.id == user_id))
    user_data = user.scalar_one_or_none()
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data





