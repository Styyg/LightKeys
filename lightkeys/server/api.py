from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any
from pathlib import Path

def get_renderer():
    """Récupère le renderer depuis app.state, ou lève une erreur propre."""
    renderer = getattr(app.state, "renderer", None)
    if renderer is None:
        raise HTTPException(status_code=500, detail="Renderer non initialisé")
    return renderer

app = FastAPI(title="LightKeys Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

web_dir = Path(__file__).parent.parent / "web"
app.mount("/web", StaticFiles(directory=web_dir), name="web")

@app.get("/")
def root():
    """Page d'accueil"""
    return FileResponse(web_dir / "index.html")

@app.get("/leds/list_color_modes")
def list_color_modes():
    """Retourne la liste des modes de couleur disponibles."""
    renderer = get_renderer()
    return {"available_modes": renderer.list_color_modes()}

@app.get("/leds/list_effect_modes")
def list_effect_modes():
    renderer = get_renderer()
    return {"available_effects": renderer.list_effect_modes()}

@app.get("/leds/color_mode")
def get_active_color_mode():
    """Retourne le mode actif et ses paramètres."""
    renderer = get_renderer()
    return {
        "active_mode": renderer.get_active_color_mode(),
        "params": renderer.get_color_params()
    }

@app.get("/leds/effect_modes")
def get_active_effect_modes():
    """Retourne les modes d'effet actifs et leurs paramètres."""
    renderer = get_renderer()
    return renderer.get_active_effect_modes()

class ModeInput(BaseModel):
    mode: str


@app.post("/leds/color_mode")
def set_color_mode(data: ModeInput):
    """Change le mode de couleur actif."""
    renderer = get_renderer()
    try:
        renderer.set_color_mode(data.mode)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"success": True, "active_mode": data.mode}

@app.post("/leds/effect_mode")
def set_effect_mode(data: ModeInput):
    """Change le mode d'effet actif."""
    renderer = get_renderer()
    try:
        renderer.set_effect_mode(data.mode)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"success": True, "active_effect": data.mode}

class ParamsInput(BaseModel):
    params: Dict[str, Any]

@app.post("/leds/color_params")
def set_color_params(data: ParamsInput):
    """Met à jour les paramètres du mode actif."""
    renderer = get_renderer()
    renderer.set_color_params(data.params)
    return {"success": True, "updated_params": data.params}

@app.post("/leds/effect_params")
def set_effect_params(data: ParamsInput):
    """Met à jour les paramètres du mode d'effet actif."""
    renderer = get_renderer()
    renderer.set_effect_params(data.params)
    return {"success": True, "updated_params": data.params}

def set_renderer(renderer):
    """Associe un objet Renderer à l'application FastAPI."""
    app.state.renderer = renderer
