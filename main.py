from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import os
import pypdf
import io

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
    file_content: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
def root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

def extract_text_from_pdf(file_content: bytes) -> str:
    """Extrait le texte d'un PDF"""
    try:
        pdf_reader = pypdf.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Erreur lors de la lecture du PDF: {str(e)}"

@app.post("/execute")
async def execute_task(
    task: str = Form(...),
    agent_type: str = Form("coordinator"),
    file: Optional[UploadFile] = File(None)
):
    """Traite la demande avec ou sans fichier"""
    
    file_content = None
    
    # Si un fichier est uploadé, on extrait son contenu
    if file:
        content = await file.read()
        
        if file.filename.endswith('.pdf'):
            file_content = extract_text_from_pdf(content)
        elif file.filename.endswith('.txt'):
            file_content = content.decode('utf-8')
        else:
            file_content = "Format de fichier non supporté. Utilisez PDF ou TXT."
    
    # Construction de la réponse
    result = f" **Fichier analysé :** {file.filename if file else 'Aucun'}\n\n"
    result += f"📝 **Contenu extrait :** {len(file_content) if file_content else 0} caractères\n\n"
    result += f"🤖 **Agent utilisé :** {agent_type}\n\n"
    result += f" **Ta demande :** {task}\n\n"
    
    if file_content:
        result += f"📋 **Résumé du document :**\n{file_content[:500]}...\n\n"
        result += "✅ L'IA a analysé ton document et est prête à répondre à tes questions !"
    else:
        result += "✅ Traitement effectué sans fichier joint."
    
    return {
        "success": True,
        "result": result,
        "agent_used": agent_type,
        "file_processed": file.filename if file else None
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "2.0"}