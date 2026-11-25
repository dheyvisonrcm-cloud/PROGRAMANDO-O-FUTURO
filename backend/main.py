from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from seguranca import gerar_hash, verificar_senha

# Importação dos nossos módulos
from database import engine, get_db, Base
import models
import schemas

# Cria as tabelas no MySQL se ainda não existirem
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Programando o Futuro - API Tourism",
    description="API do MVP de Turismo Gamificado com QR Code e Brindes Digitais",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Status"])
def home():
    return {"status": "API online", "mensagem": "Servidor FastAPI rodando com sucesso!"}


@app.get("/testar-banco", tags=["Status"])
def testar_banco(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT COUNT(*) FROM monumentos")).fetchone()
        return {
            "status": "Conexão com o MySQL OK!",
            "total_monumentos": result[0]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro de conexão: {str(e)}")



# ROTAS DE USUÁRIOS & AUTENTICAÇÃO


@app.post("/cadastrar", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED, tags=["Usuários"])
def cadastrar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    # Verifica se e-mail já existe
    usuario_existente = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado no sistema.")

    novo_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=gerar_hash(usuario.senha)
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario


@app.post("/login", response_model=schemas.TokenResponse, tags=["Usuários"])
def login(dados: schemas.LoginData, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(
        models.Usuario.email == dados.email,
        models.Usuario.senha_hash == dados.senha
    ).first()

    usuario = db.query(models.Usuario).filter(models.Usuario.email == dados.email).first()
    if not usuario or not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")
    
    return {
        "access_token": f"token_simulado_{usuario.id_usuario}",
        "token_type": "bearer",
        "usuario": usuario
    }



# ROTAS DE GAMIFICAÇÃO & RESGATE DE QR CODE


@app.post("/conquistas/resgatar", response_model=schemas.ResgateResponse, tags=["Gamificação"])
def resgatar_qrcode(payload: schemas.ResgateQRCode, db: Session = Depends(get_db)):
    # 1. Busca o usuário
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == payload.id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    # 2. Busca o monumento pelo QR Code Hash
    monumento = db.query(models.Monumento).filter(models.Monumento.qrcode_hash == payload.qrcode_hash).first()
    if not monumento:
        raise HTTPException(status_code=404, detail="QR Code / Monumento não encontrado.")

    # 3. Valida a Trava Anti-Fraude (Duplicidade)
    ja_conquistou = db.query(models.UsuarioConquista).filter(
        models.UsuarioConquista.id_usuario == payload.id_usuario,
        models.UsuarioConquista.id_monumento == monumento.id_monumento
    ).first()

    if ja_conquistou:
        raise HTTPException(status_code=400, detail="Você já resgatou os pontos deste monumento anteriormente!")

    # 4. Guarda os valores antes do commit (depois dele o SQLAlchemy recarrega os objetos)
    pontos_ganhos = monumento.pontos
    nome_monumento = monumento.nome_monumento

    # 5. Prepara a conquista
    nova_conquista = models.UsuarioConquista(
        id_usuario=payload.id_usuario,
        id_monumento=monumento.id_monumento
    )
    db.add(nova_conquista)

    # 6. Soma os pontos direto no banco: UPDATE ... SET pontos_totais = pontos_totais + X
    usuario.pontos_totais = models.Usuario.pontos_totais + pontos_ganhos

    # 7. Atribui o brinde correspondente (se houver)
    brinde = db.query(models.Brinde).filter(models.Brinde.id_monumento == monumento.id_monumento).first()
    nome_brinde_ganho = None

    if brinde:
        novo_brinde_usuario = models.UsuarioBrinde(
            id_usuario=payload.id_usuario,
            brinde_id=brinde.brinde_id
        )
        db.add(novo_brinde_usuario)
        nome_brinde_ganho = brinde.nome_brinde

    # 8. Confirma tudo de uma vez. Se a trava UNIQUE do banco barrar, desfaz tudo
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Você já resgatou os pontos deste monumento anteriormente!")

    db.refresh(usuario)

    return {
        "mensagem": "Monumento conquistado com sucesso!",
        "pontos_ganhos": pontos_ganhos,
        "total_pontos_atual": usuario.pontos_totais,
        "monumento": nome_monumento,
        "brinde_desbloqueado": nome_brinde_ganho
    }
