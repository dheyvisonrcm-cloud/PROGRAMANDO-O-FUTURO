import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Carrega as variáveis definidas no arquivo .env
load_dotenv()

# Recupera as credenciais do ambiente
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "programando_futuro")

# Monta a String de Conexão (URL) do MySQL via Driver PyMySQL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Cria o motor de conexão do SQLAlchemy com o MySQL
engine = create_engine(DATABASE_URL, echo=True)

# Cria a fábrica de sessões para executar consultas SQL
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base que será herdada pelos modelos ORM (models.py)
Base = declarative_base()

# Função Utilitária (Injeção de Dependência) para abrir e fechar conexões na API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()