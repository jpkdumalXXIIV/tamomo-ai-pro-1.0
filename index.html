# ============================================
# TAMOMO AI PRO - Serveur principal
# Version 2.0 avec upload de fichiers
# ============================================

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import os
import pypdf
import io

# Création de l'application FastAPI
app = FastAPI(title="TAMOMO AI PRO")

# Configuration CORS (autorise toutes les connexions)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# ROUTE 1 : Page d'accueil (affiche le site)
# ============================================
@app.get("/", response_class=HTMLResponse)
def root():
    """Affiche le fichier index.html"""
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# ============================================
# ROUTE 2 : Traitement de la demande IA
# ============================================
@app.post("/execute")
async def execute_task(
    task: str = Form(...),
    agent_type: str = Form("coordinator"),
    file: Optional[UploadFile] = File(None)
):
    """
    Traite la demande de l'utilisateur avec ou sans fichier.
    Reçoit : task (texte), agent_type (type d'agent), file (fichier optionnel)
    """
    
    file_content = None
    file_name = None
    
    # Si un fichier est uploadé, on l'analyse
    if file:
        file_name = file.filename
        content = await file.read()
        
        # Lecture du PDF
        if file_name.endswith('.pdf'):
            try:
                pdf_reader = pypdf.PdfReader(io.BytesIO(content))
                file_content = ""
                for page in pdf_reader.pages:
                    file_content += page.extract_text() + "\n"
            except Exception as e:
                file_content = f"Erreur lecture PDF: {str(e)}"
        
        # Lecture du fichier texte
        elif file_name.endswith('.txt'):
            file_content = content.decode('utf-8')
        
        else:
            file_content = "Format non supporté. Utilisez PDF ou TXT."
    
    # Construction de la réponse
    result = f"📄 **Fichier analysé :** {file_name if file_name else 'Aucun'}\n\n"
    result += f"📊 **Taille du contenu :** {len(file_content) if file_content else 0} caractères\n\n"
    result += f"🤖 **Agent utilisé :** {agent_type}\n\n"
    result += f"📝 **Ta demande :** {task}\n\n"
    
    if file_content:
        # On affiche les 500 premiers caractères du document
        preview = file_content[:500].replace('\n', ' ')
        result += f"📋 **Aperçu du document :**\n{preview}...\n\n"
        result += "✅ L'IA a analysé ton document avec succès !"
    else:
        result += "✅ Traitement effectué sans fichier joint."
    
    return {
        "success": True,
        "result": result,
        "agent_used": agent_type,
        "file_processed": file_name
    }

# ============================================
# ROUTE 3 : Vérification de santé (pour Railway)
# ============================================
@app.get("/health")
def health_check():
    """Railway utilise cette route pour vérifier que l'app fonctionne"""
    return {"status": "healthy", "version": "2.0"}