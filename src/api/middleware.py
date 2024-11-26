from fastapi import Request, Response
import logging
from starlette.middleware.base import BaseHTTPMiddleware

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log de la solicitud entrante
        logger.info(f"Solicitud recibida: {request.method} {request.url}")
        
        # Ejecutar el siguiente middleware o endpoint
        response = await call_next(request)
        
        # Log de la respuesta
        logger.info(f"Respuesta: {response.status_code}")
        
        return response
