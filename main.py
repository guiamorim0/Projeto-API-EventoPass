from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session, joinedload
import models
import schemas
from database import session_local, engine

models.base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

@app.post(
    '/participantes/',
    response_model= schemas.ParticipanteResponse)
def criar_participante(participante: schemas.ParticipanteCreate, db: Session = Depends(get_db)):
    existente = db.query(models.Participante).filter(models.Participante.email == participante.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="Email ja cadastrado!")

    db_participante = models.Participante(**participante.model_dump())
    db.add(db_participante)
    db.commit()
    db.refresh(db_participante)
    return db_participante

@app.get(
    '/participantes/',
    response_model= List[schemas.ParticipanteResponse])
def listar_participantes(db: Session = Depends(get_db)):
    query = db.query(models.Participante)
    return query.all()

@app.get(
    '/participantes/{participante_id}',
    response_model= schemas.ParticipanteResponse)
def ler_participante(participante_id: int, db: Session = Depends(get_db)):
    participante = db.query(models.Participante).filter(models.Participante.id == participante_id).first()
    if not participante:
        raise HTTPException(status_code=404, detail="Participante nao encontrado!")
    return participante

@app.delete('/participantes/{participante_id}')
def remover_participante(participante_id: int, db: Session = Depends(get_db)):
    participante = db.query(models.Participante).filter(models.Participante.id == participante_id).first()
    if not participante:
        raise HTTPException(status_code=404, detail="Participante nao encontrado!")
    db.delete(participante)
    db.commit()
    return {"mensagem":"Participante removido com sucesso!"}

@app.post(
    '/eventos/',
    response_model= schemas.EventoResponse)
def criar_evento(evento: schemas.EventoCreate, db: Session = Depends(get_db)):
    db_evento = models.Evento(**evento.model_dump())
    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)
    return db_evento

@app.get(
    '/eventos/',
    response_model= List[schemas.EventoResponse])
def listar_eventos(cidade: str | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Evento)
    if cidade is not None:
        query = query.filter(models.Evento.cidade == cidade)
    return query.all()

@app.get(
    '/eventos/{evento_id}',
    response_model= schemas.EventoResponse)
def ler_evento(evento_id: int, db: Session = Depends(get_db)):
    evento = db.query(models.Evento).filter(models.Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento nao encontrado!")
    return evento

@app.delete('/eventos/{evento_id}')
def remover_evento(evento_id: int, db: Session = Depends(get_db)):
    evento = db.query(models.Evento).filter(models.Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento nao encontrado!")
    db.delete(evento)
    db.commit()
    return {"mensagem":"Evento removido com sucesso!"}