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
    secret_code: str = Form(""),  # NOUVEAU : Le code VIP
    file: Optional[UploadFile] = File(None)
):
    """Traite la demande et vérifie le code VIP"""
    
    # Vérification du code VIP
    is_vip = False
    VIP_CODES = ["TAMOMO2026", "GEEK2026", "BOSS2026"] # Tes codes secrets
    
    if secret_code.upper() in VIP_CODES:
        is_vip = True
    
    file_content = None
    file_name = None
    
    # Analyse du fichier
    if file:
        file_name = file.filename
        content = await file.read()
        if file_name.endswith('.pdf'):
            try:
                pdf_reader = pypdf.PdfReader(io.BytesIO(content))
                file_content = ""
                for page in pdf_reader.pages:
                    file_content += page.extract_text() + "\n"
            except Exception as e:
                file_content = f"Erreur lecture PDF: {str(e)}"
        elif file_name.endswith('.txt'):
            file_content = content.decode('utf-8')
        else:
            file_content = "Format non supporté."
    
    # Construction de la réponse
    badge = " **VIP ACTIVÉ** 🌟\n\n" if is_vip else " **Mode Gratuit**\n\n"
    
    result = f"{badge} **Fichier :** {file_name if file_name else 'Aucun'}\n\n"
    result += f"🤖 **Agent :** {agent_type}\n\n"
    result += f" **Demande :** {task}\n\n"
    
    if file_content:
        preview = file_content[:300].replace('\n', ' ')
        result += f"📋 **Aperçu :**\n{preview}...\n\n"
        result += "✅ Document analysé avec succès !"
    else:
        result += "✅ Traitement effectué. L'IA a généré ta réponse."
    
    return {
        "success": True,
        "result": result,
        "agent_used": agent_type,
        "file_processed": file_name,
        "is_vip": is_vip  # On renvoie l'info VIP au site
    }
# ============================================
# ROUTE 3 : Vérification de santé (pour Railway)
# ============================================
@app.get("/health")
def health_check():
    """Railway utilise cette route pour vérifier que l'app fonctionne"""
    return {"status": "healthy", "version": "2.0"}