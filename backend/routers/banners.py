from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Banner
from schemas import BannerOut

router = APIRouter(prefix="/api/banners", tags=["banners"])


@router.get("", response_model=list[BannerOut])
def list_banners(db: Session = Depends(get_db)):
    return db.query(Banner).filter(Banner.active == True).order_by(Banner.sort_order).all()
