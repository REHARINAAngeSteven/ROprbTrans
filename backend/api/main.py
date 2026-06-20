from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Ajouter le chemin du projet
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.routes import balas_hammer, stepping_stone
from api.models.schemas import HealthResponse

app = FastAPI(
    title="Transport Problem API",
    description="API pour la résolution de problèmes de transport avec Balas-Hammer et Stepping Stone",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite
        "http://localhost:3000",  # React par défaut
        "http://localhost:8080",  # Autre port possible
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(balas_hammer.router)
app.include_router(stepping_stone.router)

@app.get("/", tags=["Root"])
async def root():
    """
    Racine de l'API - affiche les informations disponibles
    """
    return {
        "message": "Transport Problem API",
        "version": "1.0.0",
        "endpoints": {
            "balas_hammer": "/balas-hammer/solve",
            "stepping_stone": "/stepping-stone/optimize",
            "documentation": "/docs"
        }
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Vérifie l'état de santé de l'API
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )