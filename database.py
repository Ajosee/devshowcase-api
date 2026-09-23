from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define onde o banco de dados gratuito (SQLite) vai ficar salvo no seu computador
SQLALCHEMY_DATABASE_URL = "sqlite:///./devshowcase.db"

# Cria o motor que vai conversar com o arquivo do banco de dados
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Cria uma fábrica de sessões para podermos salvar e buscar dados nas tabelas
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função auxiliar que abre e fecha a conexão com o banco para cada requisição da API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
