from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI(title="LightKeys Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "service": "lightkeys"}

# État temporaire du ruban
current_color = {"r": 0, "g": 0, "b": 0, "w": 0}

@app.get("/leds/color_modes")
def list_color_modes():
    """Retourne la liste des modes de couleur disponibles."""
    renderer = getattr(app.state, "renderer", None)
    if not renderer:
        raise HTTPException(status_code=500, detail="Renderer non initialisé")

    return {"available_modes": renderer.list_color_modes()}


@app.get("/leds/color_mode")
def get_color_mode():
    """Retourne le mode actif et ses paramètres."""
    renderer = getattr(app.state, "renderer", None)
    if not renderer:
        raise HTTPException(status_code=500, detail="Renderer non initialisé")

    return {
        "active_mode": renderer.get_active_color_mode(),
        "params": renderer.get_color_params()
    }


class ColorModeInput(BaseModel):
    mode: str


@app.post("/leds/color_mode")
def set_color_mode(data: ColorModeInput):
    """Change le mode de couleur actif."""
    renderer = getattr(app.state, "renderer", None)
    if not renderer:
        raise HTTPException(status_code=500, detail="Renderer non initialisé")

    try:
        renderer.set_color_mode(data.mode)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"success": True, "active_mode": data.mode}


class ColorParamsInput(BaseModel):
    params: Dict[str, Any]


@app.post("/leds/color_params")
def set_color_params(data: ColorParamsInput):
    """Met à jour les paramètres du mode actif."""
    renderer = getattr(app.state, "renderer", None)
    if not renderer:
        raise HTTPException(status_code=500, detail="Renderer non initialisé")

    renderer.set_color_params(data.params)
    return {"success": True, "updated_params": data.params}

def set_renderer(renderer):
    """Associe un objet Renderer à l'application FastAPI."""
    app.state.renderer = renderer
