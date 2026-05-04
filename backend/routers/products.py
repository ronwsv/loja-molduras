from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import Product, ProductImage
from schemas import ProductOut

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("/featured", response_model=list[ProductOut])
def list_featured(db: Session = Depends(get_db)):
    return (
        db.query(Product)
        .options(joinedload(Product.category), joinedload(Product.images))
        .filter(Product.featured == True)
        .all()
    )


@router.get("", response_model=list[ProductOut])
def list_products(
    category_id: int | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = Query(default=20, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Product).options(joinedload(Product.category), joinedload(Product.images))
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = (
        db.query(Product)
        .options(joinedload(Product.category), joinedload(Product.images))
        .filter(Product.id == product_id)
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product
