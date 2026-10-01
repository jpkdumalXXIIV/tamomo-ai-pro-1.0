# ============================================
# MODÈLES DE DONNÉES (Les "Formulaires")
# ============================================
# Ce fichier définit la "forme" des données qui entrent et sortent de ton API.

from pydantic import BaseModel, Field
from typing import Optional

# ============================================
# MODÈLES D'ENTRÉE (ce que l'utilisateur envoie)
# ============================================

class TaskRequest(BaseModel):
    """
    Ce que l'utilisateur doit envoyer pour demander un traitement.
    
    Exemple de ce qu'il envoie :
    {
        "task": "Écris un article sur les chats",
        "agent_type": "coordinator"
    }
    """
    task: str = Field(
        ...,  # ... signifie "ce champ est obligatoire"
        description="La tâche à exécuter",
        min_length=3,
        max_length=10000,
        examples=["Écris un article sur l'intelligence artificielle"]
    )
    
    agent_type: str = Field(
        default="coordinator",
        description="Le type d'agent à utiliser (coordinator, researcher, writer)",
        examples=["coordinator"]
    )

# ============================================
# MODÈLES DE SORTIE (ce que l'API renvoie)
# ============================================

class TaskResponse(BaseModel):
    """
    La réponse renvoyée après traitement d'une tâche.
    """
    success: bool = Field(description="Est-ce que la tâche a réussi ? (True ou False)")
    result: str = Field(description="Le texte résultat du traitement")
    agent_used: str = Field(description="Le nom de l'agent qui a fait le travail")

class AgentResponse(BaseModel):
    """
    Informations sur un agent disponible (utilisé pour la liste des agents).
    """
    name: str = Field(description="Le nom de l'agent")
    description: str = Field(description="Ce que fait l'agent")
    status: str = Field(description="Statut de l'agent (active, inactive, error)")

class HealthResponse(BaseModel):
    """
    Réponse du check de santé (utilisé par Railway pour vérifier que ton site est vivant).
    """
    status: str = Field(description="État de l'application (healthy ou degraded)")
    version: str = Field(description="Version de l'application")
    openai_configured: bool = Field(description="Est-ce que la clé OpenAI est bien là ?")