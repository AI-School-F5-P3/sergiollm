import streamlit as st
import pandas as pd
import altair as alt

def render():
    st.title("Métricas y Análisis")
    
    # Ejemplo de datos ficticios
    data = pd.DataFrame({
        "Tipo de Contenido": ["Blog", "Twitter", "LinkedIn", "Instagram"],
        "Cantidad Generada": [50, 75, 30, 40],
    })
    
    # Gráfico interactivo
    chart = alt.Chart(data).mark_bar().encode(
        x="Tipo de Contenido",
        y="Cantidad Generada",
        color="Tipo de Contenido"
    )
    
    st.altair_chart(chart, use_container_width=True)
