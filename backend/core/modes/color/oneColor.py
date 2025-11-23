from .base import ColorMode
from .params import ParamDef, ParamType
import logging

log = logging.getLogger("OneColor")

class OneColor(ColorMode):
    name = "One Color"
    description = "All notes use the same color."
    schema = {
        "color": {"type": "color", "label": "Color"}
    }

    def __init__(self, color=(255, 0, 0, 0)):
        self.color = color

    def get_color(self, msg: dict) -> tuple[int, int, int, int]:
        if self.color == (0, 0, 0, 0):
            log.warning("OneColor mode with color (0,0,0,0)")
        return self.color
    
    def get_params_def(cls):
        return [
            ParamDef(
                name="one-color",
                label="One Color",
                type="color",
                default="#ffffff",
            )
        ]
    
    def update_params(self, params):
        log.debug(f"{self.name}.update_params with {params}")
        self.color = tuple(params.get("color", self.color))

    def get_params(self):
        return self.color