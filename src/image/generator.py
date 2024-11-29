from typing import Optional
import torch
from diffusers import DiffusionPipeline
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import logging
import os
from huggingface_hub import login
import time

# Configurar variables de entorno
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:512'

class ImageGenerator:
    """Generador de imágenes usando Hugging Face, Stable Diffusion local o Unsplash."""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Configurar sesión de requests con reintentos
        self.session = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        self.session.mount('http://', HTTPAdapter(max_retries=retries))
        self.session.mount('https://', HTTPAdapter(max_retries=retries))
        
        # Inicializar Hugging Face pipeline si el token está disponible
        self.pipe = None
        if self.config.huggingface_token:
            self._initialize_pipeline()

    def _initialize_pipeline(self):
        """Inicializa el pipeline de difusión con manejo de errores."""
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                login(token=self.config.huggingface_token)
                
                # Forzar modo CPU si la GPU tiene poca memoria
                device = "cpu"  # Cambio a CPU por defecto
                self.logger.info(f"Usando dispositivo: {device}")
                
                # Inicializar el pipeline con configuración más robusta
                self.pipe = DiffusionPipeline.from_pretrained(
                    "stabilityai/stable-diffusion-3.5-large",
                    torch_dtype=torch.float32,  # Usar float32 en CPU
                    use_safetensors=True,
                    variant="fp16",
                    low_cpu_mem_usage=True,
                )
                
                # Optimizaciones de memoria
                self.pipe.enable_attention_slicing(slice_size="max")
                self.pipe.enable_vae_slicing()
                self.pipe.enable_model_cpu_offload()
                
                # Reducir tamaño del batch y otros parámetros que consumen memoria
                self.pipe.scheduler.batch_size = 1
                
                break  # Si llegamos aquí, la inicialización fue exitosa
                
            except Exception as e:
                self.logger.error(f"Intento {attempt + 1} fallido: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Backoff exponencial
                else:
                    self.logger.error("No se pudo inicializar el pipeline después de todos los intentos")
                    self.pipe = None

    def generate(self, prompt: str) -> Optional[str]:
        """Genera o busca una imagen basada en el prompt."""
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                # Intentar con Hugging Face primero
                if self.pipe:
                    image_path = self._generate_huggingface_image(prompt, device)
                    if image_path:
                        self.logger.info(f"Imagen generada exitosamente: {image_path}")
                        return image_path
                
                # Si falla, usar Unsplash como fallback
                self.logger.info("Usando Unsplash como fallback")
                return self._get_unsplash_image(prompt)
                
            except Exception as e:
                self.logger.error(f"Intento {attempt + 1} fallido: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    self.logger.error("Error en todos los intentos de generación")
                    return None
    
    def _generate_huggingface_image(self, prompt: str, device: str) -> Optional[str]:
        """Genera una imagen usando Hugging Face Diffusers respetando la selección de dispositivo."""
        try:
            # Configurar el dispositivo
            if device == "gpu":
                if torch.cuda.is_available():
                    self.pipe = self.pipe.to("cuda")
                    torch.cuda.empty_cache()
                else:
                    raise RuntimeError("GPU no disponible. No se puede generar imagen en GPU.")
            elif device == "cpu":
                self.pipe = self.pipe.to("cpu")
            else:
                raise ValueError(f"Dispositivo no válido: {device}. Use 'cpu' o 'gpu'.")
            
            with torch.no_grad():
                image = self.pipe(
                    prompt,
                    height=128,
                    width=128,
                    num_inference_steps=20,
                    guidance_scale=7.0,
                ).images[0]
            
            output_dir = "generated_images"
            os.makedirs(output_dir, exist_ok=True)
            
            safe_filename = "".join(c for c in prompt if c.isalnum() or c in (' ', '_'))
            safe_filename = safe_filename.replace(' ', '_')[:100]
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            output_path = os.path.join(output_dir, f"{safe_filename}_{timestamp}.png")
            
            image.save(output_path)
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error en generación de Hugging Face: {str(e)}")
            return None


    def _get_unsplash_image(self, prompt: str) -> Optional[str]:
        """Obtiene una imagen relevante de Unsplash."""
        try:
            if not self.config.unsplash_api_key:
                self.logger.error("No se encontró API key de Unsplash")
                return None
            
            response = self.session.get(
                "https://api.unsplash.com/photos/random",
                params={
                    "query": prompt,
                    "orientation": "landscape",
                },
                headers={
                    "Authorization": f"Client-ID {self.config.unsplash_api_key}"
                },
                timeout=(5, 15)  # (connect timeout, read timeout)
            )
            
            response.raise_for_status()
            
            data = response.json()
            return data["urls"]["regular"]
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error en API de Unsplash: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Error inesperado en Unsplash: {str(e)}")
            return None