# ============================================
# CLASSE DE BASE POUR TOUS LES AGENTS
# ============================================
from openai import AsyncOpenAI
import os

class BaseAgent:
    def __init__(self, api_key=None, model="gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        if self.api_key:
            self.client = AsyncOpenAI(api_key=self.api_key)
        else:
            self.client = None

    async def chat(self, system_prompt, user_message):
        if not self.client:
            return "❌ Erreur : La clé API OpenAI n'est pas configurée."
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Erreur OpenAI : {str(e)}"