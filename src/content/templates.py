from dataclasses import dataclass
from typing import Optional, Any, Dict

@dataclass
class ContentTemplate:
    """Template base para la generación de contenido."""
    platform: str
    tone: str
    max_length: int
    style: str
    requires_image: bool = False
    image_style: str = ""
    additional_instructions: str = ""

    def format_content(self, content: str, image: Optional[str] = None) -> Dict[str, Any]:
        """Formatea el contenido según las especificaciones de la plataforma."""
        formatted = {
            "text": content,
            "image": image if self.requires_image else None
        }
        return formatted

class Templates:
    """Colección de templates para diferentes plataformas."""
    
    @staticmethod
    def instagram() -> ContentTemplate:
        return ContentTemplate(
            platform="Instagram",
            tone="casual y atractivo",
            max_length=2200,  # Límite de caracteres de Instagram
            style="visual y directo",
            requires_image=True,
            image_style="estilo moderno y llamativo",
            additional_instructions="""
            - Incluye emojis relevantes
            - Usa hashtags estratégicos (máximo 30)
            - Estructura el contenido en párrafos cortos
            """
        )

    @staticmethod
    def linkedin() -> ContentTemplate:
        return ContentTemplate(
            platform="LinkedIn",
            tone="profesional y formal",
            max_length=3000,
            style="informativo y estratégico",
            requires_image=False,
            additional_instructions="""
            - Enfócate en aspectos profesionales y de negocios
            - Incluye estadísticas o datos relevantes si es posible
            - Usa formato profesional con párrafos bien estructurados
            """
        )

    @staticmethod
    def twitter() -> ContentTemplate:
        return ContentTemplate(
            platform="Twitter",
            tone="conciso y directo",
            max_length=280,
            style="conversacional",
            requires_image=False,
            additional_instructions="""
            - Sé breve y directo
            - Usa hashtags relevantes (máximo 2-3)
            - Genera engagement con preguntas o llamados a la acción
            """
        )

    @staticmethod
    def facebook() -> ContentTemplate:
        return ContentTemplate(
            platform="Facebook",
            tone="informal pero informativo",
            max_length=63206,
            style="equilibrado",
            requires_image=True,
            image_style="atractivo y relevante",
            additional_instructions="""
            - Combina texto informativo con un tono cercano
            - Incluye llamados a la acción
            - Fomenta la interacción con preguntas o encuestas
            """
        )
    @staticmethod
    def blog() -> ContentTemplate:
        return ContentTemplate(
            platform="Blog",
            tone="profesional y educativo",
            max_length=5000,
            style="artículo informativo",
            requires_image=True,
            image_style="imagen profesional relacionada con el tema",
            additional_instructions="""
            - Estructura el contenido en introducción, desarrollo y conclusión
            - Usa subtítulos para organizar las secciones principales
            - Incluye ejemplos o casos prácticos cuando sea relevante
            - Mantén un tono educativo pero accesible
            - Termina con un llamado a la acción o reflexión final
            - Optimiza para SEO usando palabras clave naturalmente
            - Incluye una meta descripción de 150-160 caracteres
            """
        )

def get_template(platform: str) -> ContentTemplate:
    """
    Obtiene el template correspondiente a la plataforma especificada.
    
    Args:
        platform (str): Nombre de la plataforma (instagram, linkedin, twitter, facebook)
        
    Returns:
        ContentTemplate: Template configurado para la plataforma
        
    Raises:
        ValueError: Si la plataforma no está soportada
    """
    templates = {
        "instagram": Templates.instagram,
        "linkedin": Templates.linkedin,
        "twitter": Templates.twitter,
        "facebook": Templates.facebook,
        "blog": Templates.blog
    }
    
    template_func = templates.get(platform.lower())
    if template_func is None:
        raise ValueError(f"Plataforma no soportada: {platform}")
        
    return template_func()