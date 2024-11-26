from fastapi import FastAPI
from api.middleware import LoggingMiddleware  # Middleware que definimos
from api.routers.user_router import router as user_router  # Router para usuarios

# Crear la instancia principal de FastAPI
app = FastAPI()

# Añadir middleware global (para todas las rutas)
app.add_middleware(LoggingMiddleware)

# Incluir los routers (para manejar las rutas de la API)
app.include_router(user_router)

# Otras configuraciones o rutas generales si es necesario
