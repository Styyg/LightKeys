from abc import ABC, abstractmethod
import logging

log = logging.getLogger("COLOR_MODES")

def interpolate_colors(color1, color2, factor: float) -> tuple[int, int, int, int]:
    """Interpole entre deux couleurs RGBA"""
    r = int(color1[0] + (color2[0] - color1[0]) * factor)
    g = int(color1[1] + (color2[1] - color1[1]) * factor)
    b = int(color1[2] + (color2[2] - color1[2]) * factor)
    w = int(color1[3] + (color2[3] - color1[3]) * factor)
    return (r, g, b, w)

class ColorMode(ABC):
    @abstractmethod
    def get_color(self, note: int) -> tuple[int, int, int, int]:
        pass

class OneColor(ColorMode):
    def __init__(self, color=(255, 0, 0, 0)):
        self.color = color

    def get_color(self, note=0) -> tuple[int, int, int, int]:
        if self.color == (0, 0, 0, 0):
            log.warning("OneColor mode with color (0,0,0,0)")
        return self.color
    
    def set_color(self, color: tuple[int, int, int, int]):
        self.color = color
    
class Gradient(ColorMode):
    def __init__(self, note_color_map: dict[int, tuple[int, int, int, int]] = None):
        self.note_color_map = note_color_map if note_color_map else {}
        self.stops = sorted(self.note_color_map.keys())

    def get_color(self, note: int) -> tuple[int, int, int, int]:    
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