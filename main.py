from fastapi import FastAPI, HTTPException, status
from schemas import Products, PostProducts, ProductUpdate


app = FastAPI()

products = [
    {"id": 1, "name": "Смартфон Xiaomi Redmi Note 12", "price": 25999, "category": "Электроника", "brand": "Xiaomi"},
    {"id": 2, "name": "Ноутбук ASUS VivoBook 15", "price": 49999, "category": "Электроника", "brand": "ASUS"},
    {"id": 3, "name": "Беспроводные наушники Sony WH-1000XM4", "price": 19999, "category": "Электроника", "brand": "Sony"},
    {"id": 4, "name": "Игровая мышь Logitech G502", "price": 5999, "category": "Электроника", "brand": "Logitech"},
    
    {"id": 5, "name": "Холодильник Samsung RB37A5000SA", "price": 69999, "category": "Бытовая техника", "brand": "Samsung"},
    {"id": 6, "name": "Микроволновка LG MS-2042DB", "price": 7999, "category": "Бытовая техника", "brand": "LG"},
    {"id": 7, "name": "Пылесос Dyson V11", "price": 39999, "category": "Бытовая техника", "brand": "Dyson"},
    {"id": 8, "name": "Электрочайник Tefal KO8508", "price": 4999, "category": "Бытовая техника", "brand": "Tefal"},

    {"id": 9, "name": "Кроссовки Nike Air Force 1", "price": 12999, "category": "Одежда и обувь", "brand": "Nike"},
    {"id": 10, "name": "Джинсы Levi’s 501", "price": 8999, "category": "Одежда и обувь", "brand": "Levi’s"},
    {"id": 11, "name": "Куртка The North Face", "price": 15999, "category": "Одежда и обувь", "brand": "The North Face"},
    {"id": 12, "name": "Спортивный костюм Adidas Originals", "price": 10999, "category": "Одежда и обувь", "brand": "Adidas"},

    {"id": 13, "name": "Шоколад Milka (100 г)", "price": 199, "category": "Продукты питания", "brand": "Milka"},
    {"id": 14, "name": "Кофе Jacobs Monarch (250 г)", "price": 599, "category": "Продукты питания", "brand": "Jacobs"},
    {"id": 15, "name": "Молоко Parmalat 3,5% (1 л)", "price": 129, "category": "Продукты питания", "brand": "Parmalat"},
    {"id": 16, "name": "Макароны Barilla (500 г)", "price": 249, "category": "Продукты питания", "brand": "Barilla"},

    {"id": 17, "name": "Парфюм Chanel Coco Mademoiselle", "price": 8999, "category": "Косметика и парфюмерия", "brand": "Chanel"},
    {"id": 18, "name": "Крем для лица Nivea", "price": 499, "category": "Косметика и парфюмерия", "brand": "Nivea"},
    {"id": 19, "name": "Гель для душа Axe Black", "price": 349, "category": "Косметика и парфюмерия", "brand": "Axe"},
    {"id": 20, "name": "Тушь для ресниц Maybelline Lash Sensational", "price": 699, "category": "Косметика и парфюмерия", "brand": "Maybelline"}
]
    

@app.get('/products',response_model=list[Products], summary='get all products')
async def all_products():
    return products


@app.get('/products/{product_id}',summary='get product by id')
async def one_product(product_id: int):
    if len(products) < product_id:
        raise HTTPException(status_code=404, detail='Item not found')
    return products[product_id-1]


@app.post('/products', status_code=status.HTTP_201_CREATED, response_model=Products, summary='post product')
async def post_product(product: PostProducts):
    new_product = {"id": len(products)+1, **product.model_dump()}
    products.append(new_product)
    return products[-1]


@app.delete('/products/{product_id}', status_code=status.HTTP_204_NO_CONTENT, summary='delete product by id')
async def del_product(product_id: int):
    for i in products:
        if i["id"] == product_id:
            print(product_id)
            products.pop(product_id-1)
            return

        raise HTTPException(status_code=404, detail='Item not found')


@app.patch('/products/{product_id}', summary='update product')
async def post_product(product: ProductUpdate, product_id: int):
    if len(products) < product_id:
        raise HTTPException(status_code=404, detail='Item not found')
    
    update_data = product.model_dump(exclude_unset=True)
    products[product_id-1].update(update_data)
    return products[product_id-1]