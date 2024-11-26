from typing import Dict, Any, Optional
from src.llms.llm_selector import LLMSelector
from src.image.generator import ImageGenerator
from src.content.templates import get_template
from src.translation.translator import Translator
from src.monitoring.langsmith_tracker import LangSmithTracker
from src.utils.config import Config
from src.content.validators import ContentValidator


class ContentGenerator:
    """Generador principal de contenido."""
    
    def __init__(self, config: Config):
        self.config = config
        self.llm_selector = LLMSelector(config)
        self.image_generator = ImageGenerator(config)
        self.translator = Translator(config)
        self.tracker = LangSmithTracker(config)
    
    def generate(
        self,
        platform: str,
        topic: str,
        audience: str,
        language: str = "es",
        company_info: Optional[str] = None,
        model_name: str = "local"
    ) -> Dict[str, Any]:
        """Genera contenido para una plataforma específica."""
        
        try:
            # Obtener el template adecuado
            template = get_template(platform)
            
            # Crear el prompt
            prompt = self._create_prompt(
                template,
                topic,
                audience,
                company_info
            )
            
            # Generar el contenido base
            with self.tracker.track_generation(platform, topic):
                content = self.llm_selector.generate_content(prompt, model_name)
            
            # Traducir si es necesario
            if language != "es":
                content = self.translator.translate(content, target_lang=language)
            
            # Generar imagen si el template lo requiere
            image = None
            if template.requires_image:
                image = self.image_generator.generate(
                    prompt=f"{topic} {template.image_style}"
                )
            
            # Formatear el contenido final
            formatted_content = template.format_content(
                content=content,
                image=image
            )
        
            # Validar el contenido generado
            validator = ContentValidator(self.config)
            validation_report = validator.validate_content(
                content=formatted_content["text"],
                template=template.__dict__,
                image_metadata={"style": template.image_style} if template.requires_image else None
            )
            
            if not validation_report["overall_valid"]:
                raise ValueError(f"Contenido inválido: {validation_report}")
            
            return {
                "content": formatted_content,
                "image_url": image,
                "platform": platform,
                "language": language
            }
                
        except Exception as e:
            raise Exception(f"Error en la generación de contenido: {str(e)}")
    
    def _create_prompt(
        self,
        template,
        topic: str,
        audience: str,
        company_info: Optional[str]
    ) -> str:
        """Crea el prompt para el modelo."""
        base_prompt = f"""
        Genera contenido para {template.platform} sobre el tema: {topic}.
        Audiencia objetivo: {audience}.
        
        Requisitos:
        - Tono: {template.tone}
        - Longitud máxima: {template.max_length} caracteres
        - Estilo: {template.style}
        """
        
        if company_info:
            base_prompt += f"\nInformación de la empresa/marca: {company_info}"
        
        return base_prompt + f"\n{template.additional_instructions}"