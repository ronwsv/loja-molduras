from database import engine, SessionLocal, Base
from models import Category, Product, User
from auth import hash_password

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Admin user
admin_email = "admin@moldurasnovotempo.com.br"
if not db.query(User).filter(User.email == admin_email).first():
    admin = User(
        name="Administrador",
        email=admin_email,
        hashed_password=hash_password("admin123"),
        is_admin=True,
    )
    db.add(admin)
    db.commit()
    print(f"Admin criado: {admin_email} / admin123")
else:
    print("Admin já existe")

# Clear existing data
db.query(Product).delete()
db.query(Category).delete()
db.commit()

# Categories
categories = [
    Category(name="Quadros Decorativos", slug="quadros-decorativos", image_url="https://placehold.co/400x300/1a1a1a/F5B800?text=Quadros+Decorativos"),
    Category(name="Molduras", slug="molduras", image_url="https://placehold.co/400x300/1a1a1a/F5B800?text=Molduras"),
    Category(name="Placas Decorativas", slug="placas-decorativas", image_url="https://placehold.co/400x300/1a1a1a/F5B800?text=Placas+Decorativas"),
    Category(name="Quadros Personalizados", slug="quadros-personalizados", image_url="https://placehold.co/400x300/1a1a1a/F5B800?text=Personalizados"),
    Category(name="Kits de Quadros", slug="kits-de-quadros", image_url="https://placehold.co/400x300/1a1a1a/F5B800?text=Kits+de+Quadros"),
]
db.add_all(categories)
db.commit()

# Products
products = [
    # Quadros Decorativos
    Product(name="Quadro Cidade Noturna", slug="quadro-cidade-noturna", description="Quadro decorativo com imagem da cidade à noite, perfeito para sala de estar. Impressão em alta definição com acabamento premium.", price=89.90, image_url="https://placehold.co/400x400/1a1a1a/F5B800?text=Cidade+Noturna", category_id=1, featured=True),
    Product(name="Quadro Abstrato Dourado", slug="quadro-abstrato-dourado", description="Arte abstrata em tons dourados e pretos. Design moderno e elegante para qualquer ambiente.", price=79.90, image_url="https://placehold.co/400x400/1a1a1a/F5B800?text=Abstrato+Dourado", category_id=1, featured=True),
    Product(name="Quadro Natureza Viva", slug="quadro-natureza-viva", description="Paisagem natural com cores vibrantes. Traz vida e frescor ao seu espaço.", price=69.90, image_url="https://placehold.co/400x400/1a1a1a/F5B800?text=Natureza+Viva", category_id=1, featured=True),

    # Molduras
    Product(name="Moldura Clássica Preta 30x40", slug="moldura-classica-preta-30x40", description="Moldura clássica em madeira na cor preta, tamanho 30x40cm. Ideal para fotos e gravuras.", price=45.90, image_url="https://placehold.co/400x400/1a1a1a/F5B800?text=Moldura+Preta", category_id=2, featured=True),
    Product(name="Moldura Dourada 20x30", slug="moldura-dourada-20x30", description="Moldura elegante dourada, tamanho 20x30cm. Perfeita para diplomas e certificados.", price=39.90, image_url="https://placehold.co/400x400/1a1a1a/F5B800?text=Moldura+Dourada", category_id=2, featured=False),
    Product(name="Moldura Rústica 40x50", slug="moldura-rustica-40x50", description="Moldura em estilo rústico, tamanho 40x50cm. Combina com decoração industrial.", price=59.90, image_url="https://placehold.co/400x400/1a1a1a/F5B800?text=Moldura+R%C3%BAstica", category_id=2, featured=False),

    # Placas Decorativas
    Product(name="Placa Vintage Coffee", slug="placa-vintage-coffee", description="Placa decorativa estilo vintage com tema café. Material MDF de alta qualidade.", price=34.90, image_url="https://placehold.co/400x400/1a1a1a/F5B800?text=Placa+Coffee", category_id=3, featured=True),
    Product(name="Placa Barbearia Retrô", slug="placa-barbearia-retro", description="Placa decorativa estilo barbearia retrô. Ideal para salões e barbearias.", price=29.90, image_url="https://placehold.co/400x400/1a1a1a/F5B800?text=Placa+Barbearia", category_id=3, featured=False),

    # Quadros Personalizados
    Product(name="Quadro Personalizado com Foto", slug="quadro-personalizado-foto", description="Envie sua foto e receba um quadro único! Impressão em canvas com acabamento profissional.", price=119.90, image_url="https://placehold.co/400x400/1a1a1a/F5B800?text=Personalizado+Foto", category_id=4, featured=True),
    Product(name="Quadro Nome Personalizado", slug="quadro-nome-personalizado", description="Quadro decorativo com nome personalizado em design moderno. Ótimo para presente.", price=99.90, image_url="https://placehold.co/400x400/1a1a1a/F5B800?text=Nome+Personalizado", category_id=4, featured=False),

    # Kits
    Product(name="Kit 3 Quadros Minimalistas", slug="kit-3-quadros-minimalistas", description="Conjunto de 3 quadros com design minimalista em preto e dourado. Perfeito para compor paredes.", price=159.90, image_url="https://placehold.co/400x400/1a1a1a/F5B800?text=Kit+3+Quadros", category_id=5, featured=True),
    Product(name="Kit 5 Quadros Geométricos", slug="kit-5-quadros-geometricos", description="Conjunto de 5 quadros com formas geométricas modernas. Vários tamanhos para compor parede galeria.", price=229.90, image_url="https://placehold.co/400x400/1a1a1a/F5B800?text=Kit+5+Quadros", category_id=5, featured=False),
]
db.add_all(products)
db.commit()

print(f"Seed completo: {len(categories)} categorias, {len(products)} produtos")
db.close()
