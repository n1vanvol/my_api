from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import select, update
from app.schemas import Products, PostProducts, ProductUpdate
from app.database import get_db
from app.models import StoreProducts
from sqlalchemy.ext.asyncio import AsyncSession
from ..auth import check_role
router = APIRouter(
    tags = ['Products']
)

@router.get('/products',response_model=list[Products], summary='get all products')
async def all_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(StoreProducts).order_by(StoreProducts.id))
    products = result.scalars()
    return products


@router.get('/products/{product_id}',summary='get product by id')
async def one_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(StoreProducts).filter(StoreProducts.id == product_id))
    product = result.scalar_one_or_none()
    if product:
        return product
    raise HTTPException(status_code=404, detail='Item not found')

@router.post('/products', status_code=201, response_model=Products, summary='post product')
async def post_product(product: PostProducts, db: AsyncSession = Depends(get_db), role: str = Depends(check_role("admin"))):
    new_product = StoreProducts(**product.model_dump())
    db.add(new_product) 
    await db.commit()
    await db.refresh(new_product)
    return new_product


@router.delete('/products/{product_id}', status_code=204, summary='delete product by id')
async def del_product(product_id: int, db: AsyncSession = Depends(get_db), role: str = Depends(check_role("admin"))):
    delete_product = await db.execute(select(StoreProducts).filter(StoreProducts.id == product_id))
    product = delete_product.scalar_one_or_none()
    if product:
        await db.delete(product)
        await db.commit()
        return 
    
    raise HTTPException(status_code=404, detail='Item not found')


@router.patch('/products/{product_id}', summary='update product')
async def post_product(product: ProductUpdate, product_id: int, db: AsyncSession = Depends(get_db), role: str = Depends(check_role("admin"))):

    update_product_query = update(StoreProducts).filter(StoreProducts.id == product_id).values(**product.model_dump(exclude_unset=True)).returning(StoreProducts)
    result = await db.execute(update_product_query)

    updated_product = result.scalar_one_or_none()

    if not updated_product:
        raise HTTPException(status_code=404, detail="Item not found")

    await db.commit()

    return updated_product
        