import streamlit as st
import sys
from pathlib import Path

# Añadir el directorio raíz del proyecto al PATH
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.content.generator import ContentGenerator

def render():
    st.title("Generador de Contenido")
    
    # Inputs del usuario
    topic = st.text_input("Tema del contenido:", "")
    platform = st.selectbox("Plataforma objetivo:", ["Blog", "Instagram", "Twitter", "LinkedIn"])
    
    if st.button("Generar Contenido"):
        if topic:
            generator = ContentGenerator()  # Usa tu lógica interna
            result = generator.generate_content(topic, platform)
            st.subheader("Resultado:")
            st.write(result)
        else:
            st.error("Por favor, ingresa un tema.")
