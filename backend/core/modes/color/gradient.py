from .base import ColorMode
from .params import ParamDef, ParamType
from backend.core.math_utils import interpolate_colors
import logging

log = logging.getLogger("Gradient")

class Gradient(ColorMode):
    id = "gradient"
    name = "Gradient"
    description = "Color gradient based on note number."
    schema = {
        "steps": {
            "type": "list[object]",
            "label": "Gradient steps",
            "item_schema": {
                "note": {"type": "int", "label": "MIDI note", "min": 0, "max": 127},
                "color": {"type": "color", "label": "Associated color"}
            }
        },
        "interpolation": {
            "type": "enum",
            "label": "Interpolation",
            "options": ["linear", "cosine"]
        }
    }

    def __init__(self, note_color_map: dict[int, tuple[int, int, int, int]] = None):
        self.note_color_map = note_color_map if note_color_map else {}
        self.stops = sorted(self.note_color_map.keys())

    def get_color(self, msg: dict) -> tuple[int, int, int, int]:
        note = msg.note
        if note <= self.stops[0]:
            return self.note_color_map[self.stops[0]]
        
        if note >= self.stops[-1]:
            return self.note_color_map[self.stops[-1]]

        for i in range(1, len(self.stops)):
            if note < self.stops[i]:
                factor = (note - self.stops[i-1]) / (self.stops[i] - self.stops[i-1])
                return interpolate_colors(self.note_color_map[self.stops[i-1]], self.note_color_map[self.stops[i]], factor)

        log.error("Should not reach here in Gradient.get_color")
        return (0, 0, 0, 0) # Fallback
    
    def get_params_def(cls):
        return [
            ParamDef(
                name="steps",
                label="Gradient Steps",
                type=ParamType.LIST,
                item_schema=ParamDef(
                    name="step",
                    label="Étape",
                    type=ParamType.OBJECT,
                    default=None,
                    fields=[
                        ParamDef(
                            name="note",
                            label="Note MIDI",
                            type=ParamType.INT,
                            default=55,
                            min=0,
                            max=127
                        ),
                        ParamDef(
                            name="color",
                            label="Couleur",
                            type=ParamType.COLOR,
                            default="#FFFFFF"
                        ),
                    ]
                )
            ),
            ParamDef(
                name="interpolation",
                label="Interpolation",
                type=ParamType.ENUM,
                options=["linear", "ease_in", "ease_out"],
            ),
        ]
    
    def update_params(self, params):
        log.debug(f"{self.name}.update_params with {params}")
        self.note_color_map = {int(k): tuple(v) for k, v in params.items()}
        self.stops = sorted(self.note_color_map.keys())
        
    def get_params(self):
        return self.note_color_map
 