from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.content.generator import ContentGenerator
from src.utils.config import Config
from typing import Dict

# Inicializamos el router
router = APIRouter()

class ContentRequest(BaseModel):
    topic: str
    platform: str
    language: str
    audience: str
    company_info: str = None

class ContentResponse(BaseModel):
    content: Dict[str, str]
    image_url: str = None
    platform: str
    language: str

@router.post("/generate-content", response_model=ContentResponse)
async def generate_content(request: ContentRequest):
    """Genera contenido para una plataforma específica"""
    
    try:
        # Cargar la configuración
        config = Config()
        config.validate()  # Validar configuración
        
        # Inicializar el generador de contenido
        generator = ContentGenerator(config=config)
        
        # Generar el contenido
        result = generator.generate(
            platform=request.platform.lower(),
            topic=request.topic,
            audience=request.audience,
            language=request.language,
            company_info=request.company_info
        )
        
        return ContentResponse(
            content=result["content"],
            image_url=result.get("image_url"),
            platform=result["platform"],
            language=result["language"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar contenido: {str(e)}")
