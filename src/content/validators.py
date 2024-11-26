from typing import Dict, Any, Optional
from src.utils.config import Config

class ContentValidator:
    """Validador de contenido generado."""
    
    def __init__(self, config: Config):
        """
        Inicializa el validador.
        
        Args:
            config (Config): Configuración de la aplicación
        """
        self.config = config

    def validate_content(
        self,
        content: str,
        template: Dict[str, Any],
        image_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Valida el contenido generado contra los requisitos del template.
        
        Args:
            content (str): Contenido a validar
            template (Dict[str, Any]): Template usado para la generación
            image_metadata (Optional[Dict[str, Any]]): Metadatos de la imagen si existe
            
        Returns:
            Dict[str, Any]: Reporte de validación
        """
        validation_results = {
            "length_valid": self._validate_length(content, template["max_length"]),
            "content_present": bool(content.strip()),
            "image_valid": self._validate_image(image_metadata, template["requires_image"]),
            "platform_specific": self._validate_platform_specific(content, template["platform"]),
        }
        
        # Determinar validez general
        validation_results["overall_valid"] = all(
            result for key, result in validation_results.items()
            if key != "details"
        )
        
        return validation_results

    def _validate_length(self, content: str, max_length: int) -> bool:
        """Valida la longitud del contenido."""
        return len(content) <= max_length

    def _validate_image(
        self,
        image_metadata: Optional[Dict[str, Any]],
        requires_image: bool
    ) -> bool:
        """Valida los requisitos de imagen."""
        if requires_image:
            return image_metadata is not None
        return True

    def _validate_platform_specific(self, content: str, platform: str) -> bool:
        """
        Valida requisitos específicos de cada plataforma.
        
        Args:
            content (str): Contenido a validar
            platform (str): Plataforma para la que se generó el contenido
            
        Returns:
            bool: True si cumple los requisitos específicos de la plataforma
        """
        platform = platform.lower()
        
        if platform == "twitter":
            # Validar longitud de tweets
            return len(content) <= 280
            
        elif platform == "instagram":
            # Validar uso de hashtags y longitud
            has_hashtags = "#" in content
            return has_hashtags and len(content) <= 2200
            
        elif platform == "linkedin":
            # Validar longitud y formato profesional
            return len(content) <= 3000
            
        elif platform == "facebook":
            # Validar longitud y contenido
            return len(content) <= 63206
            
        return True  # Plataforma no especificada

    def _count_hashtags(self, content: str) -> int:
        """Cuenta el número de hashtags en el contenido."""
        return content.count("#")

    def _has_minimum_length(self, content: str, min_length: int = 50) -> bool:
        """Verifica si el contenido tiene una longitud mínima."""
        return len(content.strip()) >= min_length