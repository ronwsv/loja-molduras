import re
import io
import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session, joinedload
from PIL import Image
from database import get_db
from models import Category, Product, ProductImage, User
from schemas import CategoryIn, CategoryOut, ProductIn, ProductOut
from auth import get_admin_user

router = APIRouter(prefix="/api/admin", tags=["admin"])

UPLOADS_DIR = os.environ.get("UPLOADS_DIR", "/app/data/uploads")
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")
_ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif", "image/bmp", "image/tiff"}


def _slugify(text: str) -> str:
    s = text.lower()
    for src, dst in [("àáâãä", "a"), ("èéêë", "e"), ("ìíîï", "i"), ("òóôõö", "o"), ("ùúûü", "u"), ("ç", "c")]:
        for ch in src:
            s = s.replace(ch, dst)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def _unique_slug(base: str, db: Session, model, exclude_id: int | None = None) -> str:
    slug = base
    n = 1
    while True:
        q = db.query(model).filter(model.slug == slug)
        if exclude_id:
            q = q.filter(model.id != exclude_id)
        if not q.first():
            return slug
        slug = f"{base}-{n}"
        n += 1


# --- Image upload ---

@router.post("/upload")
async def admin_upload_image(
    file: UploadFile = File(...),
    _: User = Depends(get_admin_user),
):
    if file.content_type not in _ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Formato não suportado. Use JPG, PNG ou WebP.")
    data = await file.read()
    if len(data) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Arquivo muito grande. Máximo 10MB.")
    try:
        img = Image.open(io.BytesIO(data))
        img = img.convert("RGB")
        if img.width > 1200 or img.height > 1200:
            img.thumbnail((1200, 1200), Image.LANCZOS)
        output = io.BytesIO()
        img.save(output, format="WEBP", quality=85, method=6)
        output.seek(0)
        os.makedirs(UPLOADS_DIR, exist_ok=True)
        filename = f"{uuid.uuid4().hex}.webp"
        with open(os.path.join(UPLOADS_DIR, filename), "wb") as f:
            f.write(output.read())
        return {"url": f"{BASE_URL}/uploads/{filename}"}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="Erro ao processar imagem.")


# --- Categories ---

@router.get("/categories", response_model=list[CategoryOut])
def admin_list_categories(
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    return db.query(Category).order_by(Category.name).all()


@router.post("/categories", response_model=CategoryOut, status_code=201)
def admin_create_category(
    data: CategoryIn,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    slug = _unique_slug(_slugify(data.name), db, Category)
    cat = Category(name=data.name, slug=slug, image_url=data.image_url)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@router.put("/categories/{cat_id}", response_model=CategoryOut)
def admin_update_category(
    cat_id: int,
    data: CategoryIn,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    cat = db.query(Category).filter(Category.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    cat.name = data.name
    cat.image_url = data.image_url
    cat.slug = _unique_slug(_slugify(data.name), db, Category, exclude_id=cat_id)
    db.commit()
    db.refresh(cat)
    return cat


@router.delete("/categories/{cat_id}", status_code=204)
def admin_delete_category(
    cat_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    cat = db.query(Category).filter(Category.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    if db.query(Product).filter(Product.category_id == cat_id).first():
        raise HTTPException(status_code=400, detail="Categoria possui produtos vinculados")
    db.delete(cat)
    db.commit()


# --- Products ---

@router.get("/products", response_model=list[ProductOut])
def admin_list_products(
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    return (
        db.query(Product)
        .options(joinedload(Product.category), joinedload(Product.images))
        .order_by(Product.name)
        .all()
    )


@router.post("/products", response_model=ProductOut, status_code=201)
def admin_create_product(
    data: ProductIn,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    if not db.query(Category).filter(Category.id == data.category_id).first():
        raise HTTPException(status_code=400, detail="Categoria inválida")
    slug = _unique_slug(_slugify(data.name), db, Product)
    primary = data.images[0] if data.images else ""
    product = Product(
        name=data.name,
        slug=slug,
        description=data.description,
        image_url=primary,
        category_id=data.category_id,
        featured=data.featured,
    )
    db.add(product)
    db.flush()
    for i, url in enumerate(data.images):
        db.add(ProductImage(product_id=product.id, url=url, sort_order=i))
    db.commit()
    return (
        db.query(Product)
        .options(joinedload(Product.category), joinedload(Product.images))
        .filter(Product.id == product.id)
        .first()
    )


@router.put("/products/{product_id}", response_model=ProductOut)
def admin_update_product(
    product_id: int,
    data: ProductIn,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    if not db.query(Category).filter(Category.id == data.category_id).first():
        raise HTTPException(status_code=400, detail="Categoria inválida")
    product.name = data.name
    product.slug = _unique_slug(_slugify(data.name), db, Product, exclude_id=product_id)
    product.description = data.description
    product.image_url = data.images[0] if data.images else ""
    product.category_id = data.category_id
    product.featured = data.featured
    db.query(ProductImage).filter(ProductImage.product_id == product_id).delete()
    for i, url in enumerate(data.images):
        db.add(ProductImage(product_id=product_id, url=url, sort_order=i))
    db.commit()
    return (
        db.query(Product)
        .options(joinedload(Product.category), joinedload(Product.images))
        .filter(Product.id == product_id)
        .first()
    )


@router.delete("/products/{product_id}", status_code=204)
def admin_delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(product)
    db.commit()
