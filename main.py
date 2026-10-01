# ============================================
# TAMOMO AI PRO - Application principale
# ============================================
# Ce fichier est le "cerveau" de ton application.
# Il reçoit les demandes des utilisateurs et les envoie aux bons agents.

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# On importe nos agents (les "ouvriers" de ton IA)
# Assure-toi que le dossier "agents" et le fichier "models.py" sont bien au même endroit.
from agents.coordinator import CoordinatorAgent
from models import TaskRequest, TaskResponse, AgentResponse, HealthResponse

# ============================================
# CONFIGURATION DE L'APPLICATION
# ============================================

# On crée l'application FastAPI (le "serveur web")
app = FastAPI(
    title="TAMOMO AI PRO",
    description="Plateforme multi-agents IA pour les débutants et les geeks",
    version="1.1.0",
    docs_url="/docs",  # La page de documentation automatique
    redoc_url="/redoc" # Une autre version de la documentation
)

# Configuration CORS (permet à d'autres sites d'accéder à ton API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, tu pourras restreindre à ton domaine
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# INITIALISATION AU DÉMARRAGE
# ============================================

# Cette variable va contenir notre "chef d'orchestre" (le coordinateur)
coordinator = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Cette fonction s'exécute AU DÉMARRAGE de l'application.
    C'est ici qu'on prépare nos agents avant qu'ils ne travaillent.
    """
    global coordinator
    
    # Vérifier que la clé API OpenAI est bien présente
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️ ATTENTION : La clé OPENAI_API_KEY n'est pas définie !")
        print("   Ton IA ne pourra pas fonctionner sans elle.")
    else:
        print("✅ Clé API trouvée, initialisation des agents...")
    
    # Créer le coordinateur (le chef qui dirige les autres agents)
    coordinator = CoordinatorAgent(api_key=api_key)
    print("🚀 TAMOMO AI PRO est prêt !")
    
    yield  # L'application tourne ici
    
    # Code exécuté à l'arrêt (nettoyage)
    print("👋 Arrêt de TAMOMO AI PRO...")

# On dit à FastAPI d'utiliser cette fonction au démarrage
app.router.lifespan_context = lifespan

# ============================================
# LES ROUTES (les "pages" de ton API)
# ============================================

@app.get("/", tags="Principal")
async def accueil():
    """
    Page d'accueil simple pour vérifier que l'API fonctionne.
    """
    return {
        "message": "Bienvenue sur TAMOMO AI PRO !",
        "version": "1.1.0",
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthResponse, tags="Système")
async def health_check():
    """
    Vérifie que l'application est en bonne santé.
    Railway utilise cette route pour savoir si ton app fonctionne.
    """
    api_key_ok = bool(os.getenv("OPENAI_API_KEY"))
    return HealthResponse(
        status="healthy" if api_key_ok else "degraded",
        version="1.1.0",
        openai_configured=api_key_ok
    )

@app.post("/execute", response_model=TaskResponse, tags="Agents")
async def execute_task(request: TaskRequest):
    """
    ⭐ LA ROUTE PRINCIPALE ⭐
    C'est ici que l'utilisateur envoie sa demande.
    Le coordinateur va choisir les bons agents et leur donner du travail.
    
    Exemple d'utilisation (JSON) :
    {
        "task": "Écris-moi un article sur l'IA",
        "agent_type": "coordinator"
    }
    """
    try:
        if coordinator is None:
            raise HTTPException(
                status_code=503,
                detail="Le système n'est pas encore initialisé. Réessaie dans quelques secondes."
            )
        
        # On envoie la tâche au coordinateur
        print(f"📥 Nouvelle tâche reçue : {request.task[:50]}...")
        result = await coordinator.process(request.task, request.agent_type)
        
        return TaskResponse(
            success=True,
            result=result,
            agent_used=request.agent_type
        )
    
    except Exception as e:
        print(f"❌ Erreur : {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement : {str(e)}")

@app.get("/agents", response_model=list[AgentResponse], tags="Agents")
async def list_agents():
    """
    Liste tous les agents disponibles dans le système.
    Utile pour savoir quels "ouvriers" tu as à disposition.
    """
    return [
        AgentResponse(
            name="coordinator",
            description="Le chef d'orchestre. Il choisit les bons agents pour ta tâche.",
            status="active"
        ),
        AgentResponse(
            name="researcher",
            description="L'agent chercheur. Il trouve des informations sur un sujet.",
            status="active"
        ),
        AgentResponse(
            name="writer",
            description="L'agent rédacteur. Il écrit du contenu de qualité.",
            status="active"
        ),
    ]

# ============================================
# POINT D'ENTRÉE (pour tester en local)
# ============================================

if __name__ == "__main__":
    import uvicorn
    
    # Le port est donné par Railway (ou 8080 en local)
    port = int(os.getenv("PORT", 8080))
    
    print(f"🚀 Démarrage sur le port {port}...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False  # Pas de rechargement auto en production
    )