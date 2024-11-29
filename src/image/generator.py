from typing import Optional
from diffusers import DiffusionPipeline
import requests
import logging
import os
from huggingface_hub import login  # Importar el login


class ImageGenerator:
    """Generador de imágenes usando Hugging Face, Stable Diffusion local o Unsplash."""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Inicializar Hugging Face pipeline si el token está disponible
        self.pipe = None
        if self.config.huggingface_token:
            try:
                login(token=self.config.huggingface_token)
                self.pipe = DiffusionPipeline.from_pretrained(
                    "stabilityai/stable-diffusion-3.5-large",
                    use_auth_token=self.config.huggingface_token
                ).to("cuda")  # Usa GPU si está disponible
            except Exception as e:
                self.logger.warning(f"No se pudo cargar Hugging Face pipeline: {e}")

    def generate(self, prompt: str) -> Optional[str]:
        """Genera o busca una imagen basada en el prompt."""
        try:
            # Intentar con Hugging Face primero
            if self.pipe:
                image_path = self._generate_huggingface_image(prompt)
                if image_path:
                    return image_path
            
            # Si falla, usar Unsplash como fallback
            return self._get_unsplash_image(prompt)
            
        except Exception as e:
            self.logger.error(f"Error generando imagen: {e}")
            return None
    
    def _generate_huggingface_image(self, prompt: str) -> Optional[str]:
        """Genera una imagen usando Hugging Face Diffusers."""
        try:
            image = self.pipe(prompt, height=200, width=200).images[0]
            output_dir = "generated_images"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"{prompt.replace(' ', '_')}.png")
            image.save(output_path)
            return output_path
        except Exception as e:
            self.logger.warning(f"Hugging Face error: {e}")
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
            self.logger.error(f"Unsplash API error: {e}")
            return None
