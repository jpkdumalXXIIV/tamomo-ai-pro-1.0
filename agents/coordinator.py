# ============================================
# AGENT COORDINATEUR (Le Chef)
# ============================================
from .base import BaseAgent
from .researcher import ResearcherAgent
from .writer import WriterAgent

class CoordinatorAgent(BaseAgent):
    def __init__(self, api_key=None):
        super().__init__(api_key=api_key)
        self.researcher = ResearcherAgent(api_key=api_key)
        self.writer = WriterAgent(api_key=api_key)

    async def process(self, task, agent_type="coordinator"):
        print(f"🎯 Tâche reçue : {task[:50]}...")
        
        if agent_type == "researcher":
            return await self.researcher.research(task)
        elif agent_type == "writer":
            return await self.writer.write(task)
        else:
            return await self._smart_process(task)

    async def _smart_process(self, task):
        # Le coordinateur décide de la stratégie
        analysis_prompt = f"""Analyse cette demande et dis-moi quelle stratégie utiliser.
Demande : {task}
Réponds UNIQUEMENT avec UN de ces mots : RESEARCH, WRITE, BOTH, SIMPLE."""
        
        strategy = await self.chat("Tu es un analyseur de tâches. Réponds par UN SEUL MOT : RESEARCH, WRITE, BOTH, SIMPLE.", analysis_prompt)
        strategy = strategy.strip().upper()
        print(f"🧠 Stratégie choisie : {strategy}")

        if "RESEARCH" in strategy:
            return await self.researcher.research(task)
        elif "WRITE" in strategy:
            return await self.writer.write(task)
        elif "BOTH" in strategy:
            research = await self.researcher.research(task)
            return await self.writer.write(f"Rédige un contenu de qualité sur : {task}", context=research)
        else:
            return await self.chat("Tu es un assistant IA utile. Réponds clairement en français.", task)