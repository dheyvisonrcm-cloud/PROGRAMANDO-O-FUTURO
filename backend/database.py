import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()

# Recupera as credenciais do ambiente
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")
DB_HOST = os.getenv("DB_HOST", "")
DB_PORT = os.getenv("DB_PORT", "")
DB_NAME = os.getenv("DB_NAME", "")

DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME,
)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,   # testa a conexão antes de usar
    pool_recycle=280,     # renova conexões antes de o MySQL derrubá-las
)

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
