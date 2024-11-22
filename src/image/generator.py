from PIL import Image
from io import BytesIO
import requests

def generate_image_from_prompt(prompt):
    """Genera una imagen desde un prompt usando DALL·E u otro modelo."""
    # Aquí podrías integrar Stable Diffusion o una API externa.
    # Ejemplo: simulamos con una imagen genérica
    response = requests.get("https://via.placeholder.com/512")
    return Image.open(BytesIO(response.content))
