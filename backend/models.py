from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base


class Banner(Base):
    __tablename__ = "banners"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    subtitle = Column(String(200), default="")
    text = Column(String(300), default="")
    cta = Column(String(50), default="VER COLEÇÃO")
    image_url = Column(String(500), default="")
    sort_order = Column(Integer, default=0)
    active = Column(Boolean, default=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    image_url = Column(String(300), default="")

    products = relationship("Product", back_populates="category")


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    url = Column(String(500), nullable=False)
    sort_order = Column(Integer, default=0)

    product = relationship("Product", back_populates="images")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, index=True, nullable=False)
    description = Column(Text, default="")
    image_url = Column(String(300), default="")
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    category = relationship("Category", back_populates="products")
    images = relationship(
        "ProductImage",
        back_populates="product",
        order_by="ProductImage.sort_order",
        cascade="all, delete-orphan",
    )
