import asyncio
from database import Base, async_session, engine
from sqlalchemy import insert
from models import StoreProducts

products = [
    {"name": "Смартфон Xiaomi Redmi Note 12", "price": 25999, "quantity": 10, "category": "Электроника", "brand": "Xiaomi"},
    {"name": "iPhone 15", "price": 99999, "quantity": 5, "category": "Смартфоны", "brand": "Apple"},
    {"name": "Samsung Galaxy S23", "price": 89999, "quantity": 7, "category": "Смартфоны", "brand": "Samsung"},
    {"name": "Ноутбук MacBook Air M2", "price": 129999, "quantity": 4, "category": "Ноутбуки", "brand": "Apple"},
    {"name": "Ноутбук ASUS ROG Strix", "price": 159999, "quantity": 6, "category": "Ноутбуки", "brand": "ASUS"},
    {"name": "Игровая консоль PlayStation 5", "price": 49999, "quantity": 8, "category": "Консоли", "brand": "Sony"},
    {"name": "Игровая консоль Xbox Series X", "price": 49999, "quantity": 6, "category": "Консоли", "brand": "Microsoft"},
    {"name": "Беспроводные наушники AirPods Pro 2", "price": 24999, "quantity": 15, "category": "Аксессуары", "brand": "Apple"},
    {"name": "Наушники Sony WH-1000XM5", "price": 34999, "quantity": 10, "category": "Аксессуары", "brand": "Sony"},
    {"name": "Телевизор Samsung 4K 55\"", "price": 79999, "quantity": 3, "category": "Телевизоры", "brand": "Samsung"},
    {"name": "Телевизор LG OLED 65\"", "price": 129999, "quantity": 2, "category": "Телевизоры", "brand": "LG"}
]


async def db_drop_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        #await conn.run_sync(Base.metadata.create_all)

async def mock_data():
    async with async_session() as session:
        await session.execute(insert(StoreProducts), params=products)
        await session.commit()

        
if __name__ == "__main__":
    asyncio.run(mock_data())
