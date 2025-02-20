from sqlalchemy.orm import Mapped, mapped_column
from .database import Base


class StoreProducts(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    category: Mapped[str]= mapped_column(nullable=False)
    brand: Mapped[str]= mapped_column(nullable=False)

    def __repr__(self):
        return f"<StoreProduct(id={self.id}, name={self.name}, price={self.price}, category={self.category}, brand={self.brand})>"