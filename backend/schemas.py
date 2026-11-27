from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


# SCHEMAS DE AUTENTICAÇÃO E USUÁRIO

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str = Field(min_length=6, max_length=72)

class UsuarioResponse(BaseModel):
    id_usuario: int
    nome: str
    email: str
    pontos_totais: int

    class Config:
        from_attributes = True


class LoginData(BaseModel):
    email: EmailStr
    senha: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponse



# SCHEMAS DE MONUMENTOS E RESGATE DE QR CODE

class ResgateQRCode(BaseModel):
    qrcode_hash: str


class MissaoConcluidaResumo(BaseModel):
    titulo: str
    pontos_recompensa: int

class ResgateResponse(BaseModel):
    mensagem: str
    pontos_ganhos: int
    total_pontos_atual: int
    monumento: str
    brinde_desbloqueado: Optional[str] = None
    missoes_concluidas: List[MissaoConcluidaResumo] = []


# SCHEMAS DE INVENTÁRIO E BRINDES


class BrindeResponse(BaseModel):
    brinde_id: int
    nome_brinde: str
    imagem_url: Optional[str] = None

    class Config:
        from_attributes = True


class MeuPerfilResponse(BaseModel):
    id_usuario: int
    nome: str
    email: str
    pontos_totais: int
    monumentos_conquistados: int
    brindes: List[BrindeResponse] = []

    class Config:
        from_attributes = True
        
        
# SCHEMAS DE MAPA, NARRATIVAS E TRILHAS

class MonumentoMapa(BaseModel):
    # IMPORTANTE: não tem qrcode_hash de propósito. Ele prova que a pessoa esteve no local.
    id_monumento: int
    nome_monumento: str
    descricao_monumento: Optional[str] = None
    pontos: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        from_attributes = True


class NarrativaResponse(BaseModel):
    id_narrativa_monumento: int
    id_monumento: int
    texto_narrativa: str
    desafio: Optional[str] = None
    total_variantes: int  # o front só mostra "ver outra" se for maior que 1


class TrilhaResumo(BaseModel):
    id_trilha: int
    nome_trilha: str
    descricao_trilha: Optional[str] = None
    tema: Optional[str] = None
    total_monumentos: int


class MonumentoNaTrilha(BaseModel):
    ordem: int
    id_monumento: int
    nome_monumento: str
    descricao_monumento: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class TrilhaDetalhe(BaseModel):
    id_trilha: int
    nome_trilha: str
    descricao_trilha: Optional[str] = None
    tema: Optional[str] = None
    monumentos: List[MonumentoNaTrilha] = []
    
# SCHEMAS DE FAVORITOS E PÍLULAS SALVAS

class MensagemResponse(BaseModel):
    mensagem: str


class FavoritoResponse(BaseModel):
    id_monumento: int
    nome_monumento: str
    descricao_monumento: Optional[str] = None
    data_favorito: datetime


class NarrativaSalvaResponse(BaseModel):
    id_narrativa_monumento: int
    id_monumento: int
    nome_monumento: str
    texto_narrativa: str
    desafio: Optional[str] = None
    data_salvamento: datetime

# SCHEMAS DE PROGRESSO EM TRILHAS E MISSÕES

class EtapaProgresso(BaseModel):
    ordem: int
    id_monumento: int
    nome_monumento: str
    concluida: bool


class ProgressoTrilha(BaseModel):
    id_trilha: int
    nome_trilha: str
    status: str
    total_etapas: int
    etapas_concluidas: int
    proximo_monumento: Optional[EtapaProgresso] = None
    etapas: List[EtapaProgresso] = []


class MissaoResponse(BaseModel):
    id_missao: int
    titulo: str
    descricao_missao: str
    tipo_regra: str
    pontos_recompensa: int
    concluida: bool
    progresso: int
    total: int

class PosicaoUsuario(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class ConcluirMissaoResponse(BaseModel):
    mensagem: str
    distancia_metros: int