from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from typing import Dict, Any

class ModeInput(BaseModel):
    mode: str

class ParamsInput(BaseModel):
    params: Dict[str, Any]

def get_renderer():
    """Récupère le renderer depuis app.state, ou lève une erreur propre."""
    renderer = getattr(app.state, "renderer", None)
    if renderer is None:
        raise HTTPException(status_code=500, detail="Renderer non initialisé")
    return renderer

def set_renderer(renderer):
    """Associe un objet Renderer à l'application FastAPI."""
    app.state.renderer = renderer

app = FastAPI(title="LightKeys Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, "static")
INDEX_FILE = os.path.join(STATIC_DIR, "index.html")

# 👉 Monter le dossier static pour servir JS, CSS, etc.
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def root():
    return FileResponse(INDEX_FILE)

@app.get("/api/status")
def get_status():
    renderer = get_renderer()
    print("Getting status from renderer:", renderer)
    return {
        # "midi_connected": renderer.is_midi_connected(),
        # "leds_on": renderer.are_leds_on(),
        # "fps": renderer.get_fps()
        "midi_connected": False,
        "leds_on": False,
        "fps": renderer.FPS
    }

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

@app.get("/leds/schema")
def get_modes_schema():
    """Retourne la liste des schémas."""
    renderer = get_renderer()
    return renderer.list_mode_schemas()

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
