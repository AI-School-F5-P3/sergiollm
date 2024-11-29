import streamlit as st
import sys
from pathlib import Path

# Añadir el directorio raíz del proyecto al PATH
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.content.generator import ContentGenerator
from src.utils.config import Config  # Importar la clase Config
from src.image.generator import ImageGenerator

def render():
    st.title("Generador de Contenido")
    
    # Crear una instancia de Config
    config = Config()  # Instanciamos el config
    
    # Validar configuración antes de continuar
    try:
        config.validate()  # Validar configuración, en caso de errores en .env
    except ValueError as e:
        st.error(f"Configuración inválida: {e}")
        return
    
    # Inputs del usuario
    topic = st.text_input("Tema del contenido:", "")
    platform = st.selectbox("Plataforma objetivo:", ["Blog", "Instagram", "Twitter", "LinkedIn", "Facebook"])
    language = st.selectbox("Idioma:", ["es", "en", "fr", "de"])
    audience = st.text_input("Audiencia objetivo:", "audiencia general")
    # Selector de dispositivo (CPU/GPU)
    device = st.radio("Selecciona el dispositivo para la generación de imágenes:", ("CPU", "GPU"))
    
    if st.button("Generar Contenido"):
        if topic:
            try:
                # Inicializar generador de contenido
                generator = ContentGenerator(config=config)  # Pasar el config a ContentGenerator
                
                
                # Generar el contenido
                result = generator.generate(
                    platform=platform.lower(),  # Asegurar que coincide con los nombres de templates
                    topic=topic,
                    audience=audience,
                    language=language
                )
                
                # Mostrar el resultado
                st.subheader("Resultado:")
                st.write(result["content"]["text"])
                
                # Generar imagen usando Hugging Face
                image_generator = ImageGenerator(config=config)
                image_path = image_generator.generate(prompt=topic, device=device.lower())
                
                # Mostrar la imagen generada
                if image_path:
                    st.image(image_path, caption="Imagen generada")
                else:
                    st.warning("No se pudo generar la imagen.")
            
            except Exception as e:
                st.error(f"Error al generar contenido: {str(e)}")
        else:
            st.error("Por favor, ingresa un tema.")
