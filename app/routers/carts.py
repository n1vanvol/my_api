from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import delete, select
from ..auth import get_current_user
from ..schemas import UserInfo, AddCart, CartItemSchema
from ..models import CartItem, Carts, StoreProducts
from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter(
    tags=['Carts'],
    prefix='/cart'
)


@router.get("/")
async def my_cart(user: UserInfo = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    carts_id = await db.execute(select(Carts.id).filter(Carts.user_id == user.id))
    cart_info = carts_id.scalar_one_or_none()
    query_items = await db.execute(select(CartItem.product_id, StoreProducts.name, CartItem.quantity, StoreProducts.price).join(StoreProducts, StoreProducts.id == CartItem.product_id))
    result = query_items.all()

    items = [CartItemSchema(product_id=res[0], name= res[1], quantity=res[2], price = res[3]) for res in result]
    total_price = sum(item.quantity * item.price for item in items)
    items_dict = [item.model_dump() for item in items]


    return {"cart_id": cart_info, "user_id": user.id, "created_at": user.created_at, "items": items_dict, "total_price": total_price}


@router.post("/add_items",status_code=201)
async def add_product_to_cart(data: AddCart, user: UserInfo = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    carts_id = await db.execute(select(Carts.id).filter(Carts.user_id == user.id))
    cart_info = carts_id.scalar_one_or_none()

    query_to_products = await db.execute(select(StoreProducts).filter(StoreProducts.id == data.product_id))
    products_info = query_to_products.scalar_one_or_none()
    if not products_info:
        raise HTTPException(status_code=404, detail='Item not found')
    if products_info.quantity < data.quantity:
        raise HTTPException(status_code=400, detail="Not enough items in stock")

    existing_cart_item = await db.execute(select(CartItem).filter(CartItem.cart_id == cart_info, CartItem.product_id == data.product_id))
    items_db = existing_cart_item.scalar_one_or_none()

    if items_db and items_db.quantity + data.quantity <= products_info.quantity:
        items_db.quantity += data.quantity

    elif not items_db:
        cart_item = CartItem(cart_id=cart_info,product_id=data.product_id, quantity=data.quantity)
        db.add(cart_item)
    else:
        raise HTTPException(status_code=400, detail="Not enough items in stock")

    await db.commit()
    return {"product_id": data.product_id, "quantity": data.quantity}


@router.delete("/delete", status_code=204)
async def delete_cart(user: UserInfo = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    info = await db.execute(select(Carts).filter(Carts.user_id == user.id))
    data = info.scalar_one_or_none()
    
    await db.execute(delete(CartItem).where(CartItem.cart_id == data.id))
    await db.commit()
    return 
    