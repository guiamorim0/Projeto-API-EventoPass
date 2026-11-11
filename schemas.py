from pydantic import BaseModel
from datetime import date

class ParticipanteBase(BaseModel):
    nome: str
    email: str

class ParticipanteCreate(ParticipanteBase):
    pass

class ParticipanteResponse(ParticipanteBase):
    id: int
    class Config:
        from_attributes = True

class EventoBase(BaseModel):
    titulo: str
    cidade: str
    data: date
    vagas: int

class EventoCreate(EventoBase):
    pass

class EventoResponse(EventoBase):
    id: int
    class Config:
        from_attributes = True

class InscricaoBase(BaseModel):
    participante_id: int
    evento_id: int

class InscricaoCreate(InscricaoBase):
    pass

class InscricaoResponse(InscricaoBase):
    id: int
    class Config:
        from_attributes = True

class EventoComInscricoes(EventoResponse):
    inscricoes: list[InscricaoResponse] = []

class ParticipanteComInscricoes(ParticipanteResponse):
    inscricoes: list[InscricaoResponse] = []