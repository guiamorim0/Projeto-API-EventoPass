from sqlalchemy import Integer, String, ForeignKey, Column, Date
from sqlalchemy.orm import relationship
from database import base

class Participante(base):
    __tablename__ = 'participantes'
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    nome = Column(String)
    email = Column(
        String,
        unique=True
    )
    inscricoes = relationship("Inscricao", back_populates="participante", cascade="all, delete-orphan")

class Evento(base):
    __tablename__ = 'eventos'
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    titulo = Column(String)
    cidade = Column(String)
    data = Column(Date)
    vagas = Column(Integer)
    inscricoes = relationship("Inscricao", back_populates="evento", cascade="all, delete-orphan")

class Inscricao(base):
    __tablename__ = 'inscricoes'
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    participante_id = Column(
        Integer,
        ForeignKey('participantes.id')
    )
    evento_id = Column(
        Integer,
        ForeignKey('eventos.id')
    )
    participante = relationship("Participante", back_populates="inscricoes")
    evento = relationship("Evento", back_populates="inscricoes")

