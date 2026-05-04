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

