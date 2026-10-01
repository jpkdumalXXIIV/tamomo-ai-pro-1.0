# ============================================
# AGENT RÉDACTEUR
# ============================================
from .base import BaseAgent

class WriterAgent(BaseAgent):
    SYSTEM_PROMPT = """Tu es un rédacteur professionnel, expert en création de contenu engageant.
Quand on te demande d'écrire quelque chose, tu dois :
1. Adapter ton ton au public cible.
2. Utiliser un style clair, fluide et agréable à lire.
3. Structurer ton texte avec des paragraphes courts.
4. Éviter le jargon inutile.
Réponds toujours en français, avec un style naturel et humain."""

    async def write(self, instructions, context=""):
        user_message = instructions
        if context:
            user_message += f"\n\nContexte à utiliser :\n{context}"
        return await self.chat(self.SYSTEM_PROMPT, user_message)