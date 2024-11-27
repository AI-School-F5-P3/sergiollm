import streamlit as st
import sys
from pathlib import Path

# Añadir el directorio raíz del proyecto al PATH
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.content.generator import ContentGenerator
from src.utils.config import Config  # Importar la clase Config

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
                
                # Mostrar imagen generada, si aplica
                if result.get("image_url"):
                    st.image(result["image_url"], caption="Imagen generada")
            
            except Exception as e:
                st.error(f"Error al generar contenido: {str(e)}")
        else:
            st.error("Por favor, ingresa un tema.")
