from fastapi import APIRouter, status, HTTPException

router = APIRouter(
    tags=['Carts'],
    prefix='/cart'
)




@router.get("/{cart_id}")
async def get_cart_by_id():
    """{
    "id": 1,
    "user_id": 1,
    "items": [
        {
        "product_id": 5,
        "name": "Laptop",
        "quantity": 2,
        "price": 1200
        },
        {
        "product_id": 8,
        "name": "Mouse",
        "quantity": 1,
        "price": 30
        }
    ],
    "total_price": 2430
    }
    """
    return {}

@router.post("/add_items",status_code=201)
async def add_product_to_cart():
    """{
    "product_id": 101,
    "quantity": 1
    }
    """
    return {}

@router.delete("/", status_code=204)
async def delete_cart():
    pass