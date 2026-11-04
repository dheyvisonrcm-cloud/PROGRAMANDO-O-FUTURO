from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
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