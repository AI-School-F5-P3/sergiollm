import requests
from typing import Optional
from src.utils.config import Config
import logging

class ImageGenerator:
    """Generador de imágenes usando Stable Diffusion o Unsplash."""
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def generate(self, prompt: str) -> Optional[str]:
        """Genera o busca una imagen basada en el prompt."""
        try:
            # Intentar primero con Stable Diffusion local
            image_url = self._generate_stable_diffusion(prompt)
            if image_url:
                return image_url
            
            # Si falla, usar Unsplash como fallback
            return self._get_unsplash_image(prompt)
            
        except Exception as e:
            self.logger.error(f"Error generando imagen: {str(e)}")
            return None
    
    def _generate_stable_diffusion(self, prompt: str) -> Optional[str]:
        """Genera una imagen usando Stable Diffusion local."""
        try:
            response = requests.post(
                f"{self.config.stable_diffusion_host}/sdapi/v1/txt2img",
                json={
                    "prompt": prompt,
                    "negative_prompt": "text, watermark, low quality, blurry",
                    "steps": 30,
                    "width": 512,
                    "height": 512
                },
                timeout=30
            )
            
            if response.status_code == 200:
                # Procesar y guardar la imagen
                image_data = response.json()
                # Implementar lógica de guardado
                return "path/to/generated/image.jpg"
            
            return None
            
        except Exception as e:
            self.logger.warning(f"Stable Diffusion error: {str(e)}")
            return None
    
    def _get_unsplash_image(self, prompt: str) -> Optional[str]:
        """Obtiene una imagen relevante de Unsplash."""
        try:
            response = requests.get(
                "https://api.unsplash.com/photos/random",
                params={
                    "query": prompt,
                    "orientation": "landscape",
                },
                headers={
                    "Authorization": f"Client-ID {self.config.unsplash_api_key}"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["urls"]["regular"]
            
            return None
            
        except Exception as e:
            self.logger.error(f"Unsplash API error: {str(e)}")
            return None