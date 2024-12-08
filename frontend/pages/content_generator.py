import streamlit as st
import sys
from pathlib import Path
from PIL import Image
import time
from typing import Optional
import logging
from datetime import datetime

# Añadir el directorio raíz del proyecto al PATH
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.content.generator import ContentGenerator
from src.utils.config import Config
from src.image.generator import ImageGenerator

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentGeneratorUI:
    def __init__(self):
        self.config = Config()
        self.session_state_init()

    @staticmethod
    def session_state_init():
        """Inicializar variables de estado de la sesión"""
        if 'generation_history' not in st.session_state:
            st.session_state.generation_history = []
        if 'last_generated_time' not in st.session_state:
            st.session_state.last_generated_time = None

    def render_sidebar(self):
        """Renderizar configuraciones adicionales en la barra lateral"""
        with st.sidebar:
            st.subheader("Configuración Avanzada")
            
            # Ajustes de generación
            st.slider("Temperatura de creatividad", 0.0, 1.0, 0.7, help="Controla la creatividad del contenido generado")
            st.slider("Longitud máxima", 100, 1000, 500, help="Número máximo de palabras")
            
            # Mostrar historial
            if st.session_state.generation_history:
                st.subheader("Historial de Generación")
                for entry in st.session_state.generation_history[-5:]:  # Mostrar últimos 5
                    st.text(f"{entry['timestamp']}: {entry['topic']}")

    def render_main_content(self):
        """Renderizar el contenido principal"""
        st.title("Generador de Contenido")
        
        try:
            self.config.validate()
        except ValueError as e:
            st.error(f"Error de configuración: {e}")
            st.stop()

        # Crear tabs para diferentes secciones
        tab1, tab2 = st.tabs(["Generación de Contenido", "Configuración de Plantillas"])

        with tab1:
            self.render_generation_tab()
        
        with tab2:
            self.render_template_tab()

    def render_generation_tab(self):
        """Renderizar la tab de generación de contenido"""
        with st.form("content_generation_form"):
            # Inputs mejorados
            col1, col2 = st.columns(2)
            
            with col1:
                topic = st.text_input(
                    "Tema del contenido:",
                    help="Describe el tema sobre el que quieres generar contenido"
                )
                platform = st.selectbox(
                    "Plataforma objetivo:",
                    ["Blog", "Instagram", "Twitter", "LinkedIn", "Facebook"],
                    help="Selecciona la plataforma para la que quieres generar contenido"
                )

            with col2:
                language = st.selectbox(
                    "Idioma:",
                    ["es", "en", "fr", "de"],
                    help="Selecciona el idioma del contenido"
                )
                audience = st.text_input(
                    "Audiencia objetivo:",
                    "audiencia general",
                    help="Describe tu audiencia objetivo"
                )

            submit_button = st.form_submit_button("Generar Contenido")

        if submit_button:
            self.handle_content_generation(topic, platform, language, audience)

    def handle_content_generation(self, topic: str, platform: str, language: str, audience: str):
        """Manejar la generación de contenido"""
        if not topic:
            st.error("Por favor, ingresa un tema.")
            return

        # Mostrar spinner durante la generación
        with st.spinner("Generando contenido..."):
            try:
                # Control de ratio de generación
                if self._check_rate_limit():
                    st.warning("Por favor, espera un momento antes de generar más contenido.")
                    return

                generator = ContentGenerator(config=self.config)
                result = generator.generate(
                    platform=platform.lower(),
                    topic=topic,
                    audience=audience,
                    language=language
                )

                # Guardar en historial
                self._update_history(topic)

                # Mostrar resultados en un contenedor expandible
                with st.expander("Contenido Generado", expanded=True):
                    st.markdown(result["content"]["text"])
                    
                    # Generar y mostrar imagen
                    image_path = self._generate_image(topic)
                    if image_path:
                        st.image(image_path, caption="Imagen generada")

                # Botones de acción
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("Copiar al portapapeles"):
                        st.write("Contenido copiado!")
                with col2:
                    if st.button("Descargar"):
                        self._download_content(result)
                with col3:
                    if st.button("Regenerar"):
                        st.experimental_rerun()

            except Exception as e:
                logger.error(f"Error en generación: {str(e)}", exc_info=True)
                st.error(f"Error al generar contenido: {str(e)}")

    def render_template_tab(self):
        """Renderizar la tab de configuración de plantillas"""
        st.subheader("Configuración de Plantillas")
        platform = st.selectbox("Seleccionar plataforma:", ["Blog", "Instagram", "Twitter", "LinkedIn", "Facebook"])
        template = st.text_area("Plantilla:", height=200)
        if st.button("Guardar plantilla"):
            st.success("Plantilla guardada correctamente")

    def _check_rate_limit(self) -> bool:
        """Controlar la frecuencia de generación"""
        if st.session_state.last_generated_time:
            time_diff = time.time() - st.session_state.last_generated_time
            if time_diff < 10:  # 10 segundos entre generaciones
                return True
        st.session_state.last_generated_time = time.time()
        return False

    def _update_history(self, topic: str):
        """Actualizar historial de generación"""
        st.session_state.generation_history.append({
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'topic': topic
        })

    def _generate_image(self, prompt: str) -> Optional[str]:
        """Generar imagen con manejo de errores"""
        try:
            image_generator = ImageGenerator(config=self.config)
            return image_generator.generate(prompt=prompt)
        except Exception as e:
            logger.error(f"Error en generación de imagen: {str(e)}", exc_info=True)
            st.warning("No se pudo generar la imagen.")
            return None

    @staticmethod
    def _download_content(content: dict):
        """Preparar contenido para descarga"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"content_generation_{timestamp}.txt"
        st.download_button(
            label="Confirmar descarga",
            data=str(content),
            file_name=filename,
            mime="text/plain"
        )

def render():
    """Función principal de renderizado"""
    ui = ContentGeneratorUI()
    ui.render_sidebar()
    ui.render_main_content()

if __name__ == "__main__":
    render()