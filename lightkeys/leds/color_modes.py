from abc import ABC, abstractmethod
import logging
from lightkeys.math_utils import interpolate_colors

log = logging.getLogger("COLOR_MODES")

class ColorMode(ABC):
    name = "Abstract ColorMode"

    @abstractmethod
    def get_color(self, note: int, velocity: int) -> tuple[int, int, int, int]:
        pass

    def update_params(self, params: dict):
        """Met à jour les paramètres du mode de couleur."""
        log.warning(f"update_params not implemented for {self.name}")

    def get_params(self) -> dict:
        """Retourne les paramètres du mode de couleur."""
        log.warning(f"get_params not implemented for {self.name}")
        return {}

class OneColor(ColorMode):
    name = "One Color"

    def __init__(self, color=(255, 0, 0, 0)):
        self.color = color

    def get_color(self, note: int, velocity: int) -> tuple[int, int, int, int]:
        if self.color == (0, 0, 0, 0):
            log.warning("OneColor mode with color (0,0,0,0)")
        return self.color
    
    def update_params(self, params):
        log.debug(f"{self.name}.update_params with {params}")
        self.color = tuple(params.get("color", self.color))

    def get_params(self):
        return self.color
    
class Gradient(ColorMode):
    name = "Gradient"

    def __init__(self, note_color_map: dict[int, tuple[int, int, int, int]] = None):
        self.note_color_map = note_color_map if note_color_map else {}
        self.stops = sorted(self.note_color_map.keys())

    def get_color(self, note: int, velocity: int) -> tuple[int, int, int, int]:    
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
    
    def update_params(self, params):
        log.debug(f"{self.name}.update_params with {params}")
        self.note_color_map = {int(k): tuple(v) for k, v in params.items()}
        self.stops = sorted(self.note_color_map.keys())
        
    def get_params(self):
        return self.note_color_map
    
class VelocityBased(ColorMode):
    name = "Velocity Based"

    def __init__(self, low_vel_color=(255, 0, 0, 0), high_vel_color=(255, 255, 255, 0), low_threshold=20, high_threshold=100, easing_func=None):
        self.high_vel_color = high_vel_color
        self.low_vel_color = low_vel_color
        # clamp thresholds between 0 and 127
        if high_threshold < low_threshold:
            high_threshold, low_threshold = low_threshold, high_threshold
        self.high_threshold = max(0, min(high_threshold, 127))
        self.low_threshold = max(0, min(low_threshold, 127))
        self.easing_func = easing_func

    def get_color(self, note: int, velocity: int) -> tuple[int, int, int, int]:

        if velocity >= self.high_threshold:
            return self.high_vel_color
        elif velocity <= self.low_threshold:
            return self.low_vel_color
        
        factor = (velocity - self.low_threshold) / (self.high_threshold - self.low_threshold)
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