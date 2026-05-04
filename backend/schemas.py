from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


# --- Auth ---
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str = ""


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    address: str
    is_admin: bool = False
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --- Category ---
class CategoryOut(BaseModel):
    id: int
    name: str
    slug: str
    image_url: str

    model_config = {"from_attributes": True}


# --- Product ---
class ProductImageOut(BaseModel):
    id: int
    url: str
    sort_order: int

    model_config = {"from_attributes": True}


class ProductOut(BaseModel):
    id: int
    name: str
    slug: str
    description: str
    image_url: str
    images: list[ProductImageOut] = []
    category_id: int
    category: CategoryOut | None = None
    featured: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# --- Admin: Category ---
class CategoryIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    image_url: str = ""


# --- Admin: Product ---
class ProductIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    images: list[str] = []
    category_id: int
    featured: bool = False


# --- Contact ---
class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    phone: str = ""
    message: str


# --- Review ---
class ReviewCreate(BaseModel):
    name: str
    rating: int
    comment: str


class ReviewOut(BaseModel):
    id: int
    name: str
    rating: int
    comment: str
    created_at: datetime

    model_config = {"from_attributes": True}


# --- User Update ---
class UserUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    address: str | None = None
