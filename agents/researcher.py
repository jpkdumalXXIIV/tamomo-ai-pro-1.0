# ============================================
# AGENT CHERCHEUR
# ============================================
from .base import BaseAgent

class ResearcherAgent(BaseAgent):
    SYSTEM_PROMPT = """Tu es un chercheur expert. Quand on te donne un sujet, tu dois :
1. Identifier les points clés.
2. Fournir des informations précises.
3. Structurer ta réponse avec des titres et des puces.
4. Rester objectif et factuel.
Réponds toujours en français, de manière claire et pédagogique."""

    async def research(self, topic):
        user_message = f"Fais une recherche approfondie sur le sujet suivant : {topic}"
        return await self.chat(self.SYSTEM_PROMPT, user_message)