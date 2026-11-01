from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db

# aplicação FastAPI
app = FastAPI(
    title="Programando o Futuro - API Tourism",
    description="API do MVP de Turismo Gamificado",
    version="1.0.0"
)

# Rota raiz de teste de status
@app.get("/")
def home():
    return {"status": "API online", "mensagem": "Servidor FastAPI a rodar com sucesso!"}

# Rota para testar a conexão física com o MySQL
@app.get("/testar-banco")
def testar_banco(db: Session = Depends(get_db)):
    try:
        # Executa uma consulta simples  MySQL para contar monumentos
        result = db.execute(text("SELECT COUNT(*) FROM monumentos")).fetchone()
        return {
            "status": "Conexão com o MySQL bem-sucedida!",
            "total_monumentos_cadastrados": result[0]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro ao conectar com a base de dados: {str(e)}"
        )