from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
import random
from typing import Optional
from datetime import datetime
from missoes_service import verificar_missoes, listar_missoes_com_progresso

# Importação dos nossos módulos
from database import engine, get_db, Base
import models
import schemas
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from seguranca import gerar_hash, verificar_senha, criar_token, ler_token

# Cria as tabelas no banco (Postgres/Neon) se ainda não existirem
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

bearer = HTTPBearer()


def get_current_user(
    credenciais: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
):
    id_usuario = ler_token(credenciais.credentials)
    if id_usuario is None:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário do token não existe mais.")
    return usuario

@app.get("/", tags=["Status"])
def home():
    return {"status": "API online", "mensagem": "Servidor FastAPI rodando com sucesso!"}


@app.get("/testar-banco", tags=["Status"])
def testar_banco(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT COUNT(*) FROM monumentos")).fetchone()
        return {
            "status": "Conexão com o banco OK!",
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
    usuario = db.query(models.Usuario).filter(models.Usuario.email == dados.email).first()
    if not usuario or not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")
    
    return {
        "access_token": criar_token(usuario.id_usuario),
        "token_type": "bearer",
        "usuario": usuario
    }



# ROTAS DE GAMIFICAÇÃO & RESGATE DE QR CODE


@app.post("/conquistas/resgatar", response_model=schemas.ResgateResponse, tags=["Gamificação"])
def resgatar_qrcode(
    payload: schemas.ResgateQRCode,
    usuario: models.Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    

    # 2. Busca o monumento pelo QR Code Hash
    monumento = db.query(models.Monumento).filter(models.Monumento.qrcode_hash == payload.qrcode_hash).first()
    if not monumento:
        raise HTTPException(status_code=404, detail="QR Code / Monumento não encontrado.")

    # 3. Valida a Trava Anti-Fraude (Duplicidade)
    ja_conquistou = db.query(models.UsuarioConquista).filter(
        models.UsuarioConquista.id_usuario == usuario.id_usuario,
        models.UsuarioConquista.id_monumento == monumento.id_monumento
    ).first()

    if ja_conquistou:
        raise HTTPException(status_code=400, detail="Você já resgatou os pontos deste monumento anteriormente!")

    # 4. Guarda os valores antes do commit (depois dele o SQLAlchemy recarrega os objetos)
    pontos_ganhos = monumento.pontos
    nome_monumento = monumento.nome_monumento

    # 5. Prepara a conquista
    nova_conquista = models.UsuarioConquista(
        id_usuario=usuario.id_usuario,
        id_monumento=monumento.id_monumento
    )
    db.add(nova_conquista)

    # 6. Soma os pontos direto no banco: UPDATE ... SET pontos_totais = pontos_totais + X
    usuario.pontos_totais += pontos_ganhos

    # 7. Atribui o brinde correspondente (se houver)
    brinde = db.query(models.Brinde).filter(models.Brinde.id_monumento == monumento.id_monumento).first()
    nome_brinde_ganho = None

    if brinde:
        novo_brinde_usuario = models.UsuarioBrinde(
            id_usuario=usuario.id_usuario,
            brinde_id=brinde.brinde_id
        )
        db.add(novo_brinde_usuario)
        nome_brinde_ganho = brinde.nome_brinde

    # 8. Missões: conquista, pontos e missões concluídas na mesma transação
    missoes_novas = verificar_missoes(db, usuario)
    missoes_concluidas = [
        {"titulo": m.titulo, "pontos_recompensa": m.pontos_recompensa}
        for m in missoes_novas
    ]  # montado antes do commit, que expira os objetos

    # 9. Confirma tudo de uma vez. Se a trava UNIQUE do banco barrar, desfaz tudo
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
        "brinde_desbloqueado": nome_brinde_ganho,
        "missoes_concluidas": missoes_concluidas,
    }
# ==========================================
# ROTAS DE CONSULTA E PERFIL
# ==========================================

@app.get("/usuarios/me", response_model=schemas.MeuPerfilResponse, tags=["Usuários"])
def meu_perfil(usuario: models.Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    total_conquistas = db.query(models.UsuarioConquista).filter(
        models.UsuarioConquista.id_usuario == usuario.id_usuario
    ).count()

    registros_brindes = db.query(models.UsuarioBrinde).filter(
        models.UsuarioBrinde.id_usuario == usuario.id_usuario
    ).all()
    lista_brindes = [reg.brinde for reg in registros_brindes]

    return {
        "id_usuario": usuario.id_usuario,
        "nome": usuario.nome,
        "email": usuario.email,
        "pontos_totais": usuario.pontos_totais,
        "monumentos_conquistados": total_conquistas,
        "brindes": lista_brindes,
    }
    
# ROTAS DE MAPA, NARRATIVAS E TRILHAS (sem login)


@app.get("/monumentos", response_model=List[schemas.MonumentoMapa], tags=["Mapa"])
def listar_monumentos(db: Session = Depends(get_db)):
    # Só devolve monumentos que já têm coordenadas, para aparecerem no mapa
    return db.query(models.Monumento).filter(
        models.Monumento.latitude.isnot(None),
        models.Monumento.longitude.isnot(None)
    ).all()


@app.get("/monumentos/{id_monumento}/narrativa", response_model=schemas.NarrativaResponse, tags=["Narrativas"])
def sortear_narrativa(id_monumento: int, excluir: Optional[int] = None, db: Session = Depends(get_db)):
    monumento = db.query(models.Monumento).filter(models.Monumento.id_monumento == id_monumento).first()
    if not monumento:
        raise HTTPException(status_code=404, detail="Monumento não encontrado.")

    aprovadas = db.query(models.NarrativaMonumento).filter(
        models.NarrativaMonumento.id_monumento == id_monumento,
        models.NarrativaMonumento.aprovada == True  # noqa: E712
    ).all()

    if not aprovadas:
        raise HTTPException(status_code=404, detail="O conteúdo deste monumento ainda não está disponível.")

    # "ver outra": o front manda o id da pílula atual em ?excluir=ID para não repetir
    candidatas = [n for n in aprovadas if n.id_narrativa_monumento != excluir] or aprovadas
    escolhida = random.choice(candidatas)

    return {
        "id_narrativa_monumento": escolhida.id_narrativa_monumento,
        "id_monumento": escolhida.id_monumento,
        "texto_narrativa": escolhida.texto_narrativa,
        "desafio": escolhida.desafio,
        "total_variantes": len(aprovadas),
    }


@app.get("/trilhas", response_model=List[schemas.TrilhaResumo], tags=["Trilhas"])
def listar_trilhas(db: Session = Depends(get_db)):
    resultado = []
    for t in db.query(models.Trilha).all():
        total = db.query(models.TrilhaMonumento).filter(
            models.TrilhaMonumento.id_trilha == t.id_trilha
        ).count()
        resultado.append({
            "id_trilha": t.id_trilha,
            "nome_trilha": t.nome_trilha,
            "descricao_trilha": t.descricao_trilha,
            "tema": t.tema,
            "total_monumentos": total,
        })
    return resultado


@app.get("/trilhas/{id_trilha}", response_model=schemas.TrilhaDetalhe, tags=["Trilhas"])
def detalhar_trilha(id_trilha: int, db: Session = Depends(get_db)):
    trilha = db.query(models.Trilha).filter(models.Trilha.id_trilha == id_trilha).first()
    if not trilha:
        raise HTTPException(status_code=404, detail="Trilha não encontrada.")

    linhas = (
        db.query(models.TrilhaMonumento, models.Monumento)
        .join(models.Monumento, models.Monumento.id_monumento == models.TrilhaMonumento.id_monumento)
        .filter(models.TrilhaMonumento.id_trilha == id_trilha)
        .order_by(models.TrilhaMonumento.ordem)
        .all()
    )

    return {
        "id_trilha": trilha.id_trilha,
        "nome_trilha": trilha.nome_trilha,
        "descricao_trilha": trilha.descricao_trilha,
        "tema": trilha.tema,
        "monumentos": [
            {
                "ordem": tm.ordem,
                "id_monumento": m.id_monumento,
                "nome_monumento": m.nome_monumento,
                "descricao_monumento": m.descricao_monumento,
                "latitude": m.latitude,
                "longitude": m.longitude,
            }
            for tm, m in linhas
        ],
    }

# ROTAS COM LOGIN: FAVORITOS E PÍLULAS SALVAS


@app.post("/favoritos/{id_monumento}", response_model=schemas.MensagemResponse, status_code=201, tags=["Favoritos"])
def favoritar(
    id_monumento: int,
    usuario: models.Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    monumento = db.query(models.Monumento).filter(models.Monumento.id_monumento == id_monumento).first()
    if not monumento:
        raise HTTPException(status_code=404, detail="Monumento não encontrado.")

    ja_favoritou = db.query(models.UsuarioFavorito).filter(
        models.UsuarioFavorito.id_usuario == usuario.id_usuario,
        models.UsuarioFavorito.id_monumento == id_monumento
    ).first()
    if ja_favoritou:
        raise HTTPException(status_code=400, detail="Este monumento já está nos seus favoritos.")

    db.add(models.UsuarioFavorito(id_usuario=usuario.id_usuario, id_monumento=id_monumento))
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Este monumento já está nos seus favoritos.")

    return {"mensagem": "Monumento adicionado aos favoritos."}


@app.delete("/favoritos/{id_monumento}", response_model=schemas.MensagemResponse, tags=["Favoritos"])
def desfavoritar(
    id_monumento: int,
    usuario: models.Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    favorito = db.query(models.UsuarioFavorito).filter(
        models.UsuarioFavorito.id_usuario == usuario.id_usuario,
        models.UsuarioFavorito.id_monumento == id_monumento
    ).first()
    if not favorito:
        raise HTTPException(status_code=404, detail="Este monumento não está nos seus favoritos.")

    db.delete(favorito)
    db.commit()
    return {"mensagem": "Monumento removido dos favoritos."}


@app.get("/favoritos", response_model=List[schemas.FavoritoResponse], tags=["Favoritos"])
def listar_favoritos(usuario: models.Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    linhas = (
        db.query(models.UsuarioFavorito, models.Monumento)
        .join(models.Monumento, models.Monumento.id_monumento == models.UsuarioFavorito.id_monumento)
        .filter(models.UsuarioFavorito.id_usuario == usuario.id_usuario)
        .order_by(models.UsuarioFavorito.data_favorito.desc())
        .all()
    )
    return [
        {
            "id_monumento": m.id_monumento,
            "nome_monumento": m.nome_monumento,
            "descricao_monumento": m.descricao_monumento,
            "data_favorito": f.data_favorito,
        }
        for f, m in linhas
    ]


@app.post("/narrativas/{id_narrativa_monumento}/salvar", response_model=schemas.MensagemResponse, status_code=201, tags=["Narrativas"])
def salvar_narrativa(
    id_narrativa_monumento: int,
    usuario: models.Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Só pílulas aprovadas podem ser salvas
    narrativa = db.query(models.NarrativaMonumento).filter(
        models.NarrativaMonumento.id_narrativa_monumento == id_narrativa_monumento,
        models.NarrativaMonumento.aprovada == True  # noqa: E712
    ).first()
    if not narrativa:
        raise HTTPException(status_code=404, detail="Pílula não encontrada.")

    ja_salvou = db.query(models.UsuarioNarrativa).filter(
        models.UsuarioNarrativa.id_usuario == usuario.id_usuario,
        models.UsuarioNarrativa.id_narrativa_monumento == id_narrativa_monumento
    ).first()
    if ja_salvou:
        raise HTTPException(status_code=400, detail="Você já salvou esta pílula.")

    db.add(models.UsuarioNarrativa(
        id_usuario=usuario.id_usuario,
        id_narrativa_monumento=id_narrativa_monumento
    ))
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Você já salvou esta pílula.")

    return {"mensagem": "Pílula salva no seu diário."}


@app.get("/narrativas/salvas", response_model=List[schemas.NarrativaSalvaResponse], tags=["Narrativas"])
def listar_narrativas_salvas(usuario: models.Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    linhas = (
        db.query(models.UsuarioNarrativa, models.NarrativaMonumento, models.Monumento)
        .join(models.NarrativaMonumento, models.NarrativaMonumento.id_narrativa_monumento == models.UsuarioNarrativa.id_narrativa_monumento)
        .join(models.Monumento, models.Monumento.id_monumento == models.NarrativaMonumento.id_monumento)
        .filter(models.UsuarioNarrativa.id_usuario == usuario.id_usuario)
        .order_by(models.UsuarioNarrativa.data_salvamento.desc())
        .all()
    )
    return [
        {
            "id_narrativa_monumento": n.id_narrativa_monumento,
            "id_monumento": m.id_monumento,
            "nome_monumento": m.nome_monumento,
            "texto_narrativa": n.texto_narrativa,
            "desafio": n.desafio,
            "data_salvamento": us.data_salvamento,
        }
        for us, n, m in linhas
    ]

# ROTAS COM LOGIN: PROGRESSO EM TRILHAS E MISSÕES


@app.post("/trilhas/{id_trilha}/iniciar", response_model=schemas.MensagemResponse, status_code=201, tags=["Trilhas"])
def iniciar_trilha(
    id_trilha: int,
    usuario: models.Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    trilha = db.query(models.Trilha).filter(models.Trilha.id_trilha == id_trilha).first()
    if not trilha:
        raise HTTPException(status_code=404, detail="Trilha não encontrada.")

    ja_iniciou = db.query(models.UsuarioTrilha).filter(
        models.UsuarioTrilha.id_usuario == usuario.id_usuario,
        models.UsuarioTrilha.id_trilha == id_trilha
    ).first()
    if ja_iniciou:
        raise HTTPException(status_code=400, detail="Você já iniciou esta trilha.")

    db.add(models.UsuarioTrilha(id_usuario=usuario.id_usuario, id_trilha=id_trilha))
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Você já iniciou esta trilha.")

    return {"mensagem": "Trilha iniciada! Boa exploração."}


@app.get("/trilhas/{id_trilha}/progresso", response_model=schemas.ProgressoTrilha, tags=["Trilhas"])
def progresso_trilha(
    id_trilha: int,
    usuario: models.Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    registro = db.query(models.UsuarioTrilha).filter(
        models.UsuarioTrilha.id_usuario == usuario.id_usuario,
        models.UsuarioTrilha.id_trilha == id_trilha
    ).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Você ainda não iniciou esta trilha.")

    trilha = db.query(models.Trilha).filter(models.Trilha.id_trilha == id_trilha).first()

    linhas = (
        db.query(models.TrilhaMonumento, models.Monumento)
        .join(models.Monumento, models.Monumento.id_monumento == models.TrilhaMonumento.id_monumento)
        .filter(models.TrilhaMonumento.id_trilha == id_trilha)
        .order_by(models.TrilhaMonumento.ordem)
        .all()
    )

    # Uma etapa conta como concluída quando o usuário resgatou o QR Code daquele monumento
    ids = [m.id_monumento for tm, m in linhas]
    conquistados = set()
    if ids:
        conquistados = {
            c.id_monumento
            for c in db.query(models.UsuarioConquista).filter(
                models.UsuarioConquista.id_usuario == usuario.id_usuario,
                models.UsuarioConquista.id_monumento.in_(ids)
            ).all()
        }

    etapas = [
        {
            "ordem": tm.ordem,
            "id_monumento": m.id_monumento,
            "nome_monumento": m.nome_monumento,
            "concluida": m.id_monumento in conquistados,
        }
        for tm, m in linhas
    ]
    concluidas = sum(1 for e in etapas if e["concluida"])
    proximo = next((e for e in etapas if not e["concluida"]), None)

    # Marca a trilha como concluída na primeira vez em que todas as etapas estiverem feitas
    if etapas and concluidas == len(etapas) and registro.status != "concluida":
        registro.status = "concluida"
        registro.data_conclusao = datetime.utcnow()
        db.commit()

    return {
        "id_trilha": trilha.id_trilha,
        "nome_trilha": trilha.nome_trilha,
        "status": registro.status,
        "total_etapas": len(etapas),
        "etapas_concluidas": concluidas,
        "proximo_monumento": proximo,
        "etapas": etapas,
    }


@app.get("/missoes", response_model=List[schemas.MissaoResponse], tags=["Missões"])
def listar_missoes(usuario: models.Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    # Missões são concluídas automaticamente no /conquistas/resgatar; aqui só o status/progresso
    return listar_missoes_com_progresso(db, usuario)

@app.get("/diario", tags=["Diário"])
def obter_diario(
    usuario: models.Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conquistas = (
        db.query(models.UsuarioConquista, models.Monumento)
        .join(models.Monumento, models.UsuarioConquista.id_monumento == models.Monumento.id_monumento)
        .filter(models.UsuarioConquista.id_usuario == usuario.id_usuario)
        .order_by(models.UsuarioConquista.data_conquista.desc())
        .all()
    )
    favoritos = (
        db.query(models.UsuarioFavorito, models.Monumento)
        .join(models.Monumento, models.UsuarioFavorito.id_monumento == models.Monumento.id_monumento)
        .filter(models.UsuarioFavorito.id_usuario == usuario.id_usuario)
        .all()
    )
    narrativas = (
        db.query(models.UsuarioNarrativa, models.NarrativaMonumento, models.Monumento)
        .join(models.NarrativaMonumento, models.UsuarioNarrativa.id_narrativa_monumento == models.NarrativaMonumento.id_narrativa_monumento)
        .join(models.Monumento, models.NarrativaMonumento.id_monumento == models.Monumento.id_monumento)
        .filter(models.UsuarioNarrativa.id_usuario == usuario.id_usuario)
        .all()
    )
    trilhas = (
        db.query(models.UsuarioTrilha, models.Trilha)
        .join(models.Trilha, models.UsuarioTrilha.id_trilha == models.Trilha.id_trilha)
        .filter(models.UsuarioTrilha.id_usuario == usuario.id_usuario)
        .all()
    )
    missoes = (
        db.query(models.UsuarioMissao, models.Missao)
        .join(models.Missao, models.UsuarioMissao.id_missao == models.Missao.id_missao)
        .filter(models.UsuarioMissao.id_usuario == usuario.id_usuario)
        .all()
    )

    return {
        "conquistas": [
            {
                "id_monumento": m.id_monumento,
                "nome_monumento": m.nome_monumento,
                "cidade": m.cidade,
                "data_conquista": c.data_conquista,
            }
            for c, m in conquistas
        ],
        "favoritos": [
            {
                "id_monumento": m.id_monumento,
                "nome_monumento": m.nome_monumento,
                "cidade": m.cidade,
            }
            for _, m in favoritos
        ],
        "narrativas_salvas": [
            {
                "id_narrativa_monumento": n.id_narrativa_monumento,
                "id_monumento": m.id_monumento,
                "nome_monumento": m.nome_monumento,
                "texto_narrativa": n.texto_narrativa,
                "desafio": n.desafio,
            }
            for _, n, m in narrativas
        ],
        "trilhas": [
            {
                "id_trilha": t.id_trilha,
                "nome_trilha": t.nome_trilha,
                "status": ut.status,
                "data_inicio": getattr(ut, "data_inicio", None) or getattr(ut, "iniciada_em", None),
                "data_conclusao": getattr(ut, "data_conclusao", None) or getattr(ut, "concluida_em", None),
            }
            for ut, t in trilhas
        ],
        "missoes": [
            {
                "id_missao": m.id_missao,
                "titulo": m.titulo,
                "pontos_recompensa": m.pontos_recompensa,
                "data_conclusao": getattr(um, "data_conclusao", None) or getattr(um, "concluida_em", None),
            }
            for um, m in missoes
        ],
    }