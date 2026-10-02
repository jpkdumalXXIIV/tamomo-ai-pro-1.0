from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os

app = FastAPI(title="TAMOMO AI PRO")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskRequest(BaseModel):
    task: str
    agent_type: str = "coordinator"

# Cette fonction affiche le beau design
@app.get("/", response_class=HTMLResponse)
def root():
    # On lit le fichier index.html qu'on vient de créer
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# Cette fonction reçoit les demandes du design
@app.post("/execute")
def execute_task(request: TaskRequest):
    return {
        "success": True,
        "result": f"[TEST] J'ai bien reçu ta demande : '{request.task}' avec l'agent {request.agent_type}. Le design fonctionne !",
        "agent_used": request.agent_type
    }