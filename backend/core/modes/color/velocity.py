from .base import ColorMode
from .params import ParamDef, ParamType
from backend.core.math_utils import interpolate_colors
import logging

log = logging.getLogger("Velocity")

class VelocityBased(ColorMode):
    name = "Velocity Based"
    description = "Color changes based on note velocity."
    schema = {
        "low_threshold": {"type": "int", "label": "Low Threshold", "min": 0, "max": 127},
        "high_threshold": {"type": "int", "label": "High Threshold", "min": 0, "max": 127},
        "color_low": {"type": "color", "label": "Low Color"},
        "color_high": {"type": "color", "label": "High Color"}
    }

    def __init__(self, low_vel_color=(255, 0, 0, 0), high_vel_color=(255, 255, 255, 0), low_threshold=20, high_threshold=100, easing_func=None):
        self.high_vel_color = high_vel_color
        self.low_vel_color = low_vel_color
        # clamp thresholds between 0 and 127
        if high_threshold < low_threshold:
            high_threshold, low_threshold = low_threshold, high_threshold
        self.high_threshold = max(0, min(high_threshold, 127))
        self.low_threshold = max(0, min(low_threshold, 127))
        self.easing_func = easing_func

    def get_color(self, msg: dict) -> tuple[int, int, int, int]:
        vel = msg.velocity

        if vel >= self.high_threshold:
            return self.high_vel_color
        elif vel <= self.low_threshold:
            return self.low_vel_color
        
        factor = (vel - self.low_threshold) / (self.high_threshold - self.low_threshold)
        return interpolate_colors(self.low_vel_color, self.high_vel_color, factor, self.easing_func)
    
    def update_params(self, params):
        log.debug(f"{self.name}.update_params with {params}")
        self.low_vel_color = tuple(params.get("low_vel_color", self.low_vel_color))
        self.high_vel_color = tuple(params.get("high_vel_color", self.high_vel_color))
        low_threshold = params.get("low_threshold", self.low_threshold)
        high_threshold = params.get("high_threshold", self.high_threshold)
        if high_threshold < low_threshold:
            high_threshold, low_threshold = low_threshold, high_threshold
        self.high_threshold = max(0, min(high_threshold, 127))
        self.low_threshold = max(0, min(low_threshold, 127))
        
    def get_params(self):
        return {
            "low_vel_color": self.low_vel_color,
            "high_vel_color": self.high_vel_color,
            "low_threshold": self.low_threshold,
            "high_threshold": self.high_threshold
        }