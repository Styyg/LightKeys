from fastapi import APIRouter, Request, HTTPException
from backend.api.schemas import ModeInput, ParamsInput

router = APIRouter(prefix="/modes")

def get_renderer(request: Request):
    """Récupère le renderer depuis app.state, ou lève une erreur propre."""
    renderer = getattr(request.app.state, "renderer", None)
    if renderer is None:
        raise HTTPException(status_code=500, detail="Renderer non initialisé")
    return renderer


@router.get("/list_color_modes")
def list_color_modes():
    """Retourne la liste des modes de couleur disponibles."""
    # renderer = get_renderer()
    # return {"available_modes": renderer.list_color_modes()}
    

@router.get("/leds/list_effect_modes")
def list_effect_modes():
    renderer = get_renderer()
    return {"available_effects": renderer.list_effect_modes()}

@router.get("/leds/color_mode")
def get_active_color_mode():
    """Retourne le mode actif et ses paramètres."""
    renderer = get_renderer()
    return {
        "active_mode": renderer.get_active_color_mode(),
        "params": renderer.get_color_params()
    }

@router.get("/leds/effect_modes")
def get_active_effect_modes():
    """Retourne les modes d'effet actifs et leurs paramètres."""
    renderer = get_renderer()
    return renderer.get_active_effect_modes()

@router.get("/leds/schema")
def get_modes_schema():
    """Retourne la liste des schémas."""
    renderer = get_renderer()
    return renderer.list_mode_schemas()

@router.post("/leds/color_mode")
def set_color_mode(data: ModeInput):
    """Change le mode de couleur actif."""
    renderer = get_renderer()
    try:
        renderer.set_color_mode(data.mode)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"success": True, "active_mode": data.mode}

@router.post("/leds/effect_mode")
def set_effect_mode(data: ModeInput):
    """Change le mode d'effet actif."""
    renderer = get_renderer()
    try:
        renderer.set_effect_mode(data.mode)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"success": True, "active_effect": data.mode}

@router.post("/leds/color_params")
def set_color_params(data: ParamsInput):
    """Met à jour les paramètres du mode actif."""
    renderer = get_renderer()
    renderer.set_color_params(data.params)
    return {"success": True, "updated_params": data.params}

@router.post("/leds/effect_params")
def set_effect_params(data: ParamsInput):
    """Met à jour les paramètres du mode d'effet actif."""
    renderer = get_renderer()
    renderer.set_effect_params(data.params)
    return {"success": True, "updated_params": data.params}
