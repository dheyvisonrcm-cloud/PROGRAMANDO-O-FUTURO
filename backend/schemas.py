from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime



# SCHEMAS DE AUTENTICAÇÃO E USUÁRIO

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str


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
    id_usuario: int
    qrcode_hash: str


class ResgateResponse(BaseModel):
    mensagem: str
    pontos_ganhos: int
    total_pontos_atual: int
    monumento: str
    brinde_desbloqueado: Optional[str] = None


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