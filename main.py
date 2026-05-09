from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select

from datetime import datetime
from typing import Optional


engine = create_engine("sqlite:///logs.db")


class LogAcesso (SQLModel, table=True):
    id: Optional[int] = Field(default= None, primary_key=True)
    usuario:str
    acao:str
    ip:str
    sucesso:bool
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat()) 

def criar_tabelas():
    SQLModel.metadata.create_all(engine)

app  = FastAPI(
    title = "API de logs de acesso",
    description= "Registra e consulta eventos de acesso ao sistema",
    version= "0.3.0"
)

def on_startup():
    criar_tabelas()


#logs = []

@app.get("/")
def raiz():
    return {"status": "online","mensagem": "API de log no ar!"}


@app.post ("/logs")
def registrar_logs(log:LogAcesso):
    with Session(engine) as session:
        session.add(log)
        session.commit()
        session.refresh(log)
        return {"mensagem": "Log Registrado", "log":log}    


@app.get("/logs")
def listar_logs():
    with Session(engine) as session:
        logs = session.exec(select(LogAcesso)).all()
        return {"Total": len(logs),"logs":logs}


@app.get("/logs/{log_id}")
def buscar_log(log_id:int):
    with Session(engine) as session:
        log = session.get(LogAcesso, log_id)
        if not log:
            raise HTTPException(status_code=404, detail=f"Log {log_id} não encontrado")
        return log