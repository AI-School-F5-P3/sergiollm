from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.middleware import LoggingMiddleware  # Middleware personalizado para logueo
from api.routers.user_router import router as user_router  # Router para usuarios
from fastapi.responses import JSONResponse
import logging

# Crear la instancia principal de FastAPI
app = FastAPI(
    title="API de Gestión de Usuarios",
    description="Una API para gestionar usuarios y operaciones relacionadas",
    version="1.0.0"
)

# Configuración de CORS
# Esto permite que tu API reciba solicitudes de orígenes específicos, o todos los orígenes si permitimos "*".
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las URLs, ajusta según sea necesario
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Añadir middleware global (para todas las rutas)
# El middleware se ejecutará en todas las solicitudes y respuestas
app.add_middleware(LoggingMiddleware)

# Incluir los routers (para manejar las rutas de la API)
# Aquí se agregan todos los routers definidos en otros archivos
app.include_router(user_router)

# Manejo de errores global

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logging.error(f"HTTP error occurred: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"Error: {exc.detail}"}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unexpected error occurred: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error. Please try again later."}
    )

# Puedes agregar otras configuraciones globales o rutas generales si es necesario
# Por ejemplo, agregar una ruta general para comprobar el estado de la API
@app.get("/status")
async def get_status():
    return {"status": "API está funcionando correctamente"}

