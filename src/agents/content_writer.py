from src.agents.base_agent import BaseAgent

class ContentWriterAgent(BaseAgent):
    """Agente para escribir contenido."""
    def process(self, prompt):
        return f"Generando contenido basado en el prompt: {prompt}"
