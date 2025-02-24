from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy import ForeignKey, text, TIMESTAMP
from .database import Base


class StoreProducts(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    category: Mapped[str]= mapped_column(nullable=False)
    brand: Mapped[str]= mapped_column(nullable=False)

    def __repr__(self):
        return f"StoreProduct(id={self.id}, name={self.name}, price={self.price}, category={self.category}, brand={self.brand})"



class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text("now()"))


class Carts(Base):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text("now()"))

    def __repr__(self):
        return f'Carts(id={self.id}, user_id={self.user_id}, created_at={self.created_at})'

    