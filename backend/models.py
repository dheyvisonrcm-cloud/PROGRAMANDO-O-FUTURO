from sqlalchemy import Column, Integer, String, Text, Boolean, Numeric, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    pontos_totais = Column(Integer, default=0, nullable=False)

    # Relacionamentos
    conquistas = relationship("UsuarioConquista", back_populates="usuario")
    brindes = relationship("UsuarioBrinde", back_populates="usuario")


class Monumento(Base):
    __tablename__ = "monumentos"

    id_monumento = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome_monumento = Column(String(255), nullable=False)
    descricao_monumento = Column(String(255), nullable=True)
    qrcode_hash = Column(String(255), unique=True, nullable=False, index=True)
    pontos = Column(Integer, default=10, nullable=False)
    latitude = Column(Numeric(9, 6), nullable=True)
    longitude = Column(Numeric(9, 6), nullable=True)

    # Relacionamentos
    conquistas = relationship("UsuarioConquista", back_populates="monumento")
    brindes = relationship("Brinde", back_populates="monumento")


class Brinde(Base):
    __tablename__ = "brindes"

    brinde_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_monumento = Column(Integer, ForeignKey("monumentos.id_monumento", ondelete="SET NULL"), nullable=True)
    nome_brinde = Column(String(255), nullable=False)
    imagem_url = Column(String(255), nullable=True)

    # Relacionamentos
    monumento = relationship("Monumento", back_populates="brindes")
    usuarios = relationship("UsuarioBrinde", back_populates="brinde")


class UsuarioConquista(Base):
    __tablename__ = "usuario_conquista"

    id_conquista = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="CASCADE"), nullable=False)
    id_monumento = Column(Integer, ForeignKey("monumentos.id_monumento", ondelete="CASCADE"), nullable=False)
    data_conquista = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Trava de Unicidade: impede que o mesmo usuário conquiste o mesmo monumento 2 vezes
    __table_args__ = (
        UniqueConstraint("id_usuario", "id_monumento", name="uk_usuario_monumento"),
    )

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="conquistas")
    monumento = relationship("Monumento", back_populates="conquistas")


class UsuarioBrinde(Base):
    __tablename__ = "usuario_brindes"

    id_usuario_brindes = Column(Integer, primary_key=True, index=True, autoincrement=True)
    brinde_id = Column(Integer, ForeignKey("brindes.brinde_id", ondelete="CASCADE"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="CASCADE"), nullable=False)
    data_resgate = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relacionamentos
    usuario = relationship("Usuario", back_populates="brindes")
    brinde = relationship("Brinde", back_populates="usuarios")
    
#---------------------------------------------------------------
# TRILHAS E MISSÕES (RF08)
# ---------------------------------------------------------------

class Trilha(Base):
    __tablename__ = "trilha"

    id_trilha = Column(Integer, primary_key=True, autoincrement=True)
    nome_trilha = Column(String(150), nullable=False)
    descricao_trilha = Column(String(500), nullable=True)
    tema = Column(String(100), nullable=True)


class TrilhaMonumento(Base):
    __tablename__ = "trilha_monumento"

    id_trilha_monumento = Column(Integer, primary_key=True, autoincrement=True)
    id_trilha = Column(Integer, ForeignKey("trilha.id_trilha", ondelete="CASCADE"), nullable=False)
    id_monumento = Column(Integer, ForeignKey("monumentos.id_monumento", ondelete="CASCADE"), nullable=False)
    ordem = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("id_trilha", "id_monumento", name="uq_trilha_monumento"),
        UniqueConstraint("id_trilha", "ordem", name="uq_trilha_ordem"),
    )


class Missao(Base):
    __tablename__ = "missao"

    id_missao = Column(Integer, primary_key=True, autoincrement=True)
    id_monumento = Column(Integer, ForeignKey("monumentos.id_monumento", ondelete="CASCADE"), nullable=False)
    descricao_missao = Column(String(500), nullable=False)
    tipo_missao = Column(String(50), nullable=True)
    raio_metros = Column(Integer, nullable=False, default=200)


class UsuarioTrilha(Base):
    __tablename__ = "usuario_trilha"

    id_usuario_trilha = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="CASCADE"), nullable=False)
    id_trilha = Column(Integer, ForeignKey("trilha.id_trilha", ondelete="CASCADE"), nullable=False)
    status = Column(String(20), nullable=False, default="em_andamento")  # em_andamento | concluida
    data_inicio = Column(DateTime, default=datetime.utcnow, nullable=False)
    data_conclusao = Column(DateTime, nullable=True)

    __table_args__ = (
        UniqueConstraint("id_usuario", "id_trilha", name="uq_usuario_trilha"),
    )


class UsuarioMissao(Base):
    __tablename__ = "usuario_missao"

    id_usuario_missao = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="CASCADE"), nullable=False)
    id_missao = Column(Integer, ForeignKey("missao.id_missao", ondelete="CASCADE"), nullable=False)
    data_conclusao = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("id_usuario", "id_missao", name="uq_usuario_missao"),
    )


# ---------------------------------------------------------------
# NARRATIVAS (RF07) E DIÁRIO (RF09)
# ---------------------------------------------------------------

class NarrativaMonumento(Base):
    __tablename__ = "narrativa_monumento"

    id_narrativa_monumento = Column(Integer, primary_key=True, autoincrement=True)
    id_monumento = Column(Integer, ForeignKey("monumentos.id_monumento", ondelete="CASCADE"), nullable=False)
    variante = Column(Integer, nullable=False)
    texto_narrativa = Column(String(400), nullable=False)   # pílula curta
    desafio = Column(String(200), nullable=True)
    aprovada = Column(Boolean, nullable=False, default=False)
    data_geracao = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("id_monumento", "variante", name="uq_narrativa_variante"),
    )


class UsuarioFavorito(Base):
    __tablename__ = "usuario_favorito"

    id_favorito = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="CASCADE"), nullable=False)
    id_monumento = Column(Integer, ForeignKey("monumentos.id_monumento", ondelete="CASCADE"), nullable=False)
    data_favorito = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("id_usuario", "id_monumento", name="uq_usuario_favorito"),
    )


class UsuarioNarrativa(Base):
    __tablename__ = "usuario_narrativa"

    id_usuario_narrativa = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario", ondelete="CASCADE"), nullable=False)
    id_narrativa_monumento = Column(Integer, ForeignKey("narrativa_monumento.id_narrativa_monumento", ondelete="CASCADE"), nullable=False)
    data_salvamento = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("id_usuario", "id_narrativa_monumento", name="uq_usuario_narrativa"),
    )