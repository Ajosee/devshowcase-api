from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL oficial e correta com o endereço completo e a porta para o Render localizar o seu banco de dados
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
