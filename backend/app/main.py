from fastapi import FastAPI
from app.api.routes import router as api_router
from app.utils.logging import setup_logging

# Configuración de logging
setup_logging()

# Crear la instancia de FastAPI
app = FastAPI(title="Book Integration API")

# Incluir las rutas del API
app.include_router(api_router, prefix="/api")


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Book Integration API"}

# Ejecución del servidor (solo si se ejecuta este archivo directamente)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
