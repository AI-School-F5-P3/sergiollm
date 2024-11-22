import streamlit as st
from src.main import generate_content

# Título de la app
st.title("Generador de Contenido Automático")

# Entrada del usuario
platform = st.selectbox("Plataforma", ["LinkedIn", "Twitter", "Blog"])
topic = st.text_input("Tema", placeholder="Introduce el tema del contenido")

# Botón para generar contenido
if st.button("Generar"):
    if topic:
        st.write("Generando contenido...")
        prompt = f"Escribe un post para {platform} sobre {topic}."
        content = generate_content(prompt)
        st.subheader("Contenido generado:")
        st.write(content)
    else:
        st.warning("Por favor, introduce un tema.")
