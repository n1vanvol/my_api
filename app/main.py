from fastapi import FastAPI
import uvicorn
from .routers import products, carts, users
app = FastAPI()

app.include_router(products.router)
app.include_router(carts.router)
app.include_router(users.router)


# if __name__ == "__main__":
#     uvicorn.run("app.main:app", host="0.0.0.0")