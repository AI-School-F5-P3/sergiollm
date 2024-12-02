import os
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
import torch
from PIL import Image
import numpy as np
import tempfile


class ImageGenerator:
    def __init__(self, config):
        """
        Inicializa el generador de imágenes con el modelo Stable Diffusion 2.
        
        Args:
            config: Instancia de la clase Config con las credenciales necesarias.
        """
        self.token = config.huggingface_token
        
        # Inicializar el scheduler Euler y el pipeline de Stable Diffusion
        model_id = "stabilityai/stable-diffusion-2"

        # Usar el Euler scheduler
        scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
        
        try:
            # Cargar el pipeline de Stable Diffusion con el scheduler
            self.pipeline = StableDiffusionPipeline.from_pretrained(
                model_id,
                scheduler=scheduler,
                use_auth_token=self.token,
                torch_dtype=torch.float16  # Usar fp16 para mayor eficiencia si se tiene soporte
            )
            self.pipeline = self.pipeline.to("cuda" if torch.cuda.is_available() else "cpu")
        except Exception as e:
            raise RuntimeError(f"Error al cargar el modelo de Hugging Face: {str(e)}")
    
    def generate(self, prompt: str) -> str:
        """
        Genera una imagen basada en un prompt y la guarda como archivo temporal.
        
        Args:
            prompt: Texto descriptivo para generar la imagen.
        
        Returns:
            Ruta al archivo de imagen generado.
        """
        if not prompt:
            raise ValueError("El prompt no puede estar vacío.")
        
        try:
            # Generar la imagen usando el modelo de Stable Diffusion
            image = self.pipeline(prompt=prompt).images[0]
        except Exception as e:
            raise RuntimeError(f"Error al generar la imagen con el prompt '{prompt}': {str(e)}")

        # Verificar si la imagen es del tipo correcto (PIL.Image)
        if isinstance(image, Image.Image):
            pil_image = image
        else:
            # Si no es PIL.Image.Image, convertir el tipo
            if isinstance(image, torch.Tensor):
                # Si es un tensor, convertirlo a PIL.Image
                image = image.squeeze().permute(1, 2, 0).cpu().numpy()
            if isinstance(image, np.ndarray):
                # Si es un ndarray, convertirlo a PIL.Image
                pil_image = Image.fromarray(image)
            else:
                raise RuntimeError(f"El objeto generado no es una imagen válida: {type(image)}")
        
        # Guardar la imagen en un archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            pil_image.save(temp_file.name, format="PNG")
            return temp_file.name
