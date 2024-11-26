from typing import Dict, Any
from langchain.llms import Ollama
from langchain.schema import HumanMessage
import sys
from pathlib import Path

# Añadir el directorio raíz del proyecto al PATH
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.utils.config import Config

class LLMSelector:
    """Selector y gestor de modelos de lenguaje."""
    
    def __init__(self, config: Config):
        self.config = config
        self._initialize_models()
    
    def _initialize_models(self):
        """Inicializa los modelos disponibles."""
        self.models = {
            "local": self._setup_ollama(),
            "groq": self._setup_groq()
        }
    
    def _setup_ollama(self):
        """Configura el modelo local de Ollama."""
        return Ollama(
            base_url=self.config.ollama_host,
            model="llama2",
            temperature=0.7
        )
    
    def _setup_groq(self):
        """Configura el modelo de Groq."""
        return ChatGroq(
            api_key=self.config.groq_api_key,
            temperature=0.7,
            model_name="mixtral-8x7b-32768"
        )
    
    def get_model(self, model_name: str = "local"):
        """Obtiene un modelo específico."""
        if model_name not in self.models:
            raise ValueError(f"Modelo no disponible: {model_name}")
        return self.models[model_name]
    
    def generate_content(self, prompt: str, model_name: str = "local") -> str:
        """Genera contenido usando el modelo especificado."""
        model = self.get_model(model_name)
        
        try:
            if model_name == "groq":
                response = model.invoke([HumanMessage(content=prompt)])
                return response.content
            else:
                return model.invoke(prompt)
        except Exception as e:
            raise Exception(f"Error generando contenido: {str(e)}")