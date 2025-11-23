from fastapi import APIRouter, Request, HTTPException
from backend.api.schemas import ModeInput, ParamsInput

router = APIRouter()

def get_renderer(request: Request):
    """Récupère le renderer depuis app.state, ou lève une erreur propre."""
    renderer = getattr(request.app.state, "renderer", None)
    if renderer is None:
        raise HTTPException(status_code=500, detail="Renderer non initialisé")
    return renderer


@router.get("/status")
def get_status(request: Request):
    renderer = get_renderer(request)
    return {
        # "midi_connected": renderer.is_midi_connected(),
        # "leds_on": renderer.are_leds_on(),
        # "fps": renderer.get_fps()
        "midi_connected": False,
        "leds_on": False,
        "fps": renderer.FPS
    }