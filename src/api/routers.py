from fastapi import FastAPI
from api.middleware import LoggingMiddleware
from api.routers import user_router

app = FastAPI()

# Añadir middleware global
app.add_middleware(LoggingMiddleware)

# Incluir los routers
app.include_router(user_router)
