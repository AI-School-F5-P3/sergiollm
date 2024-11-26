from typing import Dict, Any
from deep_translator import GoogleTranslator
from src.utils.config import Config

class Translator:
    """Clase para manejar traducciones de contenido."""

    def __init__(self, config: Config):
        """
        Inicializa el traductor.
        
        Args:
            config (Config): Configuración de la aplicación
        """
        self.config = config

    def translate(self, content: str, target_lang: str) -> str:
        """
        Traduce el contenido al idioma especificado.
        
        Args:
            content (str): Contenido a traducir
            target_lang (str): Idioma destino
            
        Returns:
            str: Contenido traducido
            
        Raises:
            Exception: Si hay un error en la traducción
        """
        try:
            # Inicializar el traductor
            translator = GoogleTranslator(
                source='es',  # Idioma fuente fijo como español según generator.py
                target=target_lang
            )
            
            # Realizar la traducción
            translated_content = translator.translate(content)
            
            return translated_content
            
        except Exception as e:
            raise Exception(f"Error en la traducción: {str(e)}")