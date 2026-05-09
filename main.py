from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime


app  = FastAPI(
    title = "API de logs de acesso",
    description= "Registra e consulta eventos de acesso ao sistema",
    version= "0.2.0"
)


class LogAcesso (BaseModel):
    usuario:str
    acao:str
    ip:str
    sucesso:bool

logs = []

@app.get("/")
def raiz():
    return {"status": "online","mensagem": "API de log no ar!"}


@app.post ("/logs")
def registrar_logs(log:LogAcesso):
    novo_log = {
        "id" : len(logs) + 1,
        "usuario": log.usuario,
        "acao": log.acao,
        "ip": log.ip,
        "sucesso": log.sucesso,
        "timestamp": datetime.now().isoformat(),
    }

    logs.append(novo_log)
    return {"mensagem": "Log registrado!", "log": novo_log}
@app.get("/logs")
def listar_logs():
    return {"total": len(logs), "logs":logs}