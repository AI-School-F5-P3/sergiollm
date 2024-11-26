from fastapi import Request, Response
import logging

# Middleware para loguear las solicitudes
class LoggingMiddleware:
    async def __call__(self, request: Request, call_next):
        logging.info(f"Solicitud recibida: {request.method} {request.url}")
        response = await call_next(request)
        logging.info(f"Respuesta: {response.status_code}")
        return response
