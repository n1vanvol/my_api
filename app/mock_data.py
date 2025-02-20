import asyncio
from database import Base, async_session, engine
from sqlalchemy import insert
from models import StoreProducts


async def db_drop_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        #await conn.run_sync(Base.metadata.create_all)

async def data():
    async with async_session() as session:
        await session.execute(insert(StoreProducts), params=[
        {"name": "Смартфон Xiaomi Redmi Note 12", "price": 25999, "category": "Электроника", "brand": "Xiaomi"},
        {"name": "Ноутбук ASUS VivoBook 15", "price": 49999, "category": "Электроника", "brand": "ASUS"},
        {"name": "Беспроводные наушники Sony WH-1000XM4", "price": 19999, "category": "Электроника", "brand": "Sony"},
        { "name": "Игровая мышь Logitech G502", "price": 5999, "category": "Электроника", "brand": "Logitech"},
        
        { "name": "Холодильник Samsung RB37A5000SA", "price": 69999, "category": "Бытовая техника", "brand": "Samsung"},
        {"name": "Микроволновка LG MS-2042DB", "price": 7999, "category": "Бытовая техника", "brand": "LG"},
        { "name": "Пылесос Dyson V11", "price": 39999, "category": "Бытовая техника", "brand": "Dyson"},
        {"name": "Электрочайник Tefal KO8508", "price": 4999, "category": "Бытовая техника", "brand": "Tefal"},

        {"name": "Кроссовки Nike Air Force 1", "price": 12999, "category": "Одежда и обувь", "brand": "Nike"},
        { "name": "Джинсы Levi’s 501", "price": 8999, "category": "Одежда и обувь", "brand": "Levi’s"},
        { "name": "Куртка The North Face", "price": 15999, "category": "Одежда и обувь", "brand": "The North Face"},
        { "name": "Спортивный костюм Adidas Originals", "price": 10999, "category": "Одежда и обувь", "brand": "Adidas"},

        { "name": "Шоколад Milka (100 г)", "price": 199, "category": "Продукты питания", "brand": "Milka"},
        { "name": "Кофе Jacobs Monarch (250 г)", "price": 599, "category": "Продукты питания", "brand": "Jacobs"},
        { "name": "Молоко Parmalat 3,5% (1 л)", "price": 129, "category": "Продукты питания", "brand": "Parmalat"},
        { "name": "Макароны Barilla (500 г)", "price": 249, "category": "Продукты питания", "brand": "Barilla"},

        { "name": "Парфюм Chanel Coco Mademoiselle", "price": 8999, "category": "Косметика и парфюмерия", "brand": "Chanel"},
        { "name": "Крем для лица Nivea", "price": 499, "category": "Косметика и парфюмерия", "brand": "Nivea"},
        { "name": "Гель для душа Axe Black", "price": 349, "category": "Косметика и парфюмерия", "brand": "Axe"},
        {"name": "Тушь для ресниц Maybelline Lash Sensational", "price": 699, "category": "Косметика и парфюмерия", "brand": "Maybelline"}
        ])
        await session.commit()

        
if __name__ == "__main__":
    asyncio.run(db_drop_all())
