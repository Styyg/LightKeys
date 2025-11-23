from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.base import router

app = FastAPI(title="LightKeys Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

def set_renderer(renderer):
    """Associe un objet Renderer à l'application FastAPI."""
    app.state.renderer = renderer