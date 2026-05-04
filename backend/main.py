from fastapi import FastAPI
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import engine, Base
from routers import users, products, categories, admin

UPLOADS_DIR = os.environ.get("UPLOADS_DIR", "/app/data/uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Molduras Novo Tempo API", version="1.0.0")

_cors_origins = os.environ.get("CORS_ORIGINS", "http://localhost:3000")
allowed_origins = [o.strip() for o in _cors_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(admin.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}


app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")
