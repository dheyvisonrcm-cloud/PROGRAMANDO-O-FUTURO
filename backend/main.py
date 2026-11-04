from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from fastapi.middleware.cors import CORSMiddleware

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
    allow_credentials=True,
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
        senha_hash=usuario.senha  # Em produção usaremos hash/bcrypt
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

    if not usuario:
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

    # 4. Grava a conquista no banco
    nova_conquista = models.UsuarioConquista(
        id_usuario=payload.id_usuario,
        id_monumento=monumento.id_monumento
    )
    db.add(nova_conquista)

    # 5. Soma os pontos no perfil do usuário
    usuario.pontos_totais += monumento.pontos

    # 6. Atribui o brinde correspondente (se houver)
    brinde = db.query(models.Brinde).filter(models.Brinde.id_monumento == monumento.id_monumento).first()
    nome_brinde_ganho = None

    if brinde:
        novo_brinde_usuario = models.UsuarioBrinde(
            id_usuario=payload.id_usuario,
            brinde_id=brinde.brinde_id
        )
        db.add(novo_brinde_usuario)
        nome_brinde_ganho = brinde.nome_brinde

    db.commit()
    db.refresh(usuario)

    return {
        "mensagem": "Monumento conquistado com sucesso!",
        "pontos_ganhos": monumento.pontos,
        "total_pontos_atual": usuario.pontos_totais,
        "monumento": monumento.nome_monumento,
        "brinde_desbloqueado": nome_brinde_ganho
    }



# ROTAS DE CONSULTA E PERFIL


@app.get("/usuarios/{id_usuario}/meu-perfil", response_model=schemas.MeuPerfilResponse, tags=["Usuários"])
def meu_perfil(id_usuario: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    total_conquistas = db.query(models.UsuarioConquista).filter(models.UsuarioConquista.id_usuario == id_usuario).count()

    # Busca brindes do usuário
    registros_brindes = db.query(models.UsuarioBrinde).filter(models.UsuarioBrinde.id_usuario == id_usuario).all()
    lista_brindes = [reg.brinde for reg in registros_brindes]

    return {
        "id_usuario": usuario.id_usuario,
        "nome": usuario.nome,
        "email": usuario.email,
        "pontos_totais": usuario.pontos_totais,
        "monumentos_conquistados": total_conquistas,
        "brindes": lista_brindes
    }