from typing import Dict, Any
from langchain.llms import Ollama
from langchain.llms import OpenAI  # Importamos la clase de OpenAI
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
        """Inicializa los modelos disponibles según la configuración de la API."""
        self.models = {
            "local": self._setup_model()  # Usamos el modelo adecuado dependiendo de la configuración
        }
    
    def _setup_model(self):
        """Configura el modelo según la configuración en .env/config.py."""
        # Revisamos si el proveedor es Ollama o OpenAI
        if self.config.llm_provider == "ollama":
            return self._setup_ollama()
        elif self.config.llm_provider == "openai":
            return self._setup_openai()
        else:
            raise ValueError("Proveedor de LLM no soportado: {}".format(self.config.llm_provider))
    
    def _setup_ollama(self):
        """Configura el modelo local de Ollama."""
        return Ollama(
            base_url=self.config.ollama_host,
            model="llama2",  # Puedes cambiar a otro modelo si lo prefieres
            temperature=0.7
        )
    
    def _setup_openai(self):
        """Configura el modelo de OpenAI mediante su API."""
        return OpenAI(
            api_key=self.config.openai_api_key,  # Usamos la API Key de OpenAI desde el config
            model="gpt-4",  # Puedes elegir entre gpt-3.5, gpt-4, etc.
            temperature=0.7
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
            # Generar el contenido dependiendo del modelo seleccionado
            if isinstance(model, Ollama):
                response = model.invoke(prompt)
            elif isinstance(model, OpenAI):
                response = model.invoke([HumanMessage(content=prompt)])
            else:
                raise ValueError("Modelo no soportado para generación de contenido")
            
            return response
        except Exception as e:
            raise Exception(f"Error generando contenido: {str(e)}")
