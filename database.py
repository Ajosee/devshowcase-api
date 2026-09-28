from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Mantemos a sua lógica exata, apenas colocando o endereço completo para o servidor do Render aceitar
SQLALCHEMY_DATABASE_URL = "postgresql://postgres.lvaqcckibeojqecxqptx:AntonioMaximilio2026@://supabase.com"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
