import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
import numpy as np

def generate_sample_data():
    """Genera datos de ejemplo más realistas para el dashboard"""
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    platforms = ['Blog', 'Twitter', 'LinkedIn', 'Instagram', 'Facebook']
    
    data = []
    for date in dates:
        for platform in platforms:
            data.append({
                'fecha': date,
                'plataforma': platform,
                'generaciones': np.random.randint(5, 50),
                'tiempo_generacion': np.random.randint(2, 15),
                'tokens_generados': np.random.randint(100, 1000),
                'errores': np.random.randint(0, 3),
                'satisfaccion': np.random.uniform(3.5, 5.0)
            })
    
    return pd.DataFrame(data)

def create_trend_chart(df, metric):
    """Crea un gráfico de tendencias para una métrica específica"""
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('fecha:T', title='Fecha'),
        y=alt.Y(f'{metric}:Q', title=metric.replace('_', ' ').title()),
        color=alt.Color('plataforma:N', title='Plataforma'),
        tooltip=['fecha', 'plataforma', metric]
    ).properties(height=300)
    
    return chart

def create_platform_comparison(df, metric):
    """Crea un gráfico de comparación entre plataformas"""
    latest_data = df.groupby('plataforma')[metric].mean().reset_index()
    
    chart = alt.Chart(latest_data).mark_bar().encode(
        x=alt.X('plataforma:N', title='Plataforma'),
        y=alt.Y(f'{metric}:Q', title=metric.replace('_', ' ').title()),
        color='plataforma:N',
        tooltip=['plataforma', metric]
    ).properties(height=300)
    
    return chart

def render():
    st.title("📊 Dashboard de Métricas y Análisis")
    
    # Generar datos de ejemplo
    df = generate_sample_data()
    
    # Filtros en la barra lateral
    st.sidebar.header("Filtros")
    
    # Selector de rango de fechas
    date_range = st.sidebar.date_input(
        "Rango de fechas",
        value=(df['fecha'].min(), df['fecha'].max()),
        min_value=df['fecha'].min().to_pydatetime(),
        max_value=df['fecha'].max().to_pydatetime()
    )
    
    # Selector de plataformas
    platforms = st.sidebar.multiselect(
        "Plataformas",
        options=df['plataforma'].unique(),
        default=df['plataforma'].unique()
    )
    
    # Filtrar datos
    mask = (df['fecha'].dt.date >= date_range[0]) & (df['fecha'].dt.date <= date_range[1])
    filtered_df = df[mask & df['plataforma'].isin(platforms)]
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Generaciones",
            f"{filtered_df['generaciones'].sum():,}",
            f"{filtered_df['generaciones'].mean():.1f} promedio/día"
        )
    
    with col2:
        st.metric(
            "Tiempo Promedio",
            f"{filtered_df['tiempo_generacion'].mean():.1f}s",
            f"{filtered_df['tiempo_generacion'].std():.1f}s desv."
        )
    
    with col3:
        st.metric(
            "Tasa de Error",
            f"{(filtered_df['errores'].sum() / len(filtered_df) * 100):.1f}%",
            "del total de generaciones"
        )
    
    with col4:
        st.metric(
            "Satisfacción",
            f"{filtered_df['satisfaccion'].mean():.1f}/5",
            f"±{filtered_df['satisfaccion'].std():.2f}"
        )
    
    # Tabs para diferentes visualizaciones
    tab1, tab2, tab3 = st.tabs(["Tendencias", "Comparativas", "Datos"])
    
    with tab1:
        st.subheader("Tendencias por Plataforma")
        metric = st.selectbox(
            "Selecciona métrica",
            ['generaciones', 'tiempo_generacion', 'tokens_generados', 'errores', 'satisfaccion'],
            format_func=lambda x: x.replace('_', ' ').title()
        )
        trend_chart = create_trend_chart(filtered_df, metric)
        st.altair_chart(trend_chart, use_container_width=True)
    
    with tab2:
        st.subheader("Comparativa entre Plataformas")
        col1, col2 = st.columns(2)
        
        with col1:
            # Generaciones por plataforma
            comparison_chart = create_platform_comparison(filtered_df, 'generaciones')
            st.altair_chart(comparison_chart, use_container_width=True)
        
        with col2:
            # Tiempo promedio por plataforma
            time_chart = create_platform_comparison(filtered_df, 'tiempo_generacion')
            st.altair_chart(time_chart, use_container_width=True)
    
    with tab3:
        st.subheader("Datos Detallados")
        # Agregar búsqueda y filtros
        search = st.text_input("Buscar por plataforma:", "")
        
        if search:
            display_df = filtered_df[filtered_df['plataforma'].str.contains(search, case=False)]
        else:
            display_df = filtered_df
            
        st.dataframe(
            display_df.sort_values('fecha', ascending=False),
            use_container_width=True,
            height=400
        )
        
        # Botón de descarga
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Descargar datos",
            csv,
            "metricas.csv",
            "text/csv",
            key='download-csv'
        )

if __name__ == "__main__":
    render()