from abc import ABC, abstractmethod
import logging
import math

log = logging.getLogger("COLOR_MODES")

def ease_in_out_sin(t: float) -> float:
    """Démarre et finit en douceur"""
    return 0.5 - 0.5 * math.cos(math.pi * t)

def ease_in_out_exp(t: float) -> float:
    """Interpolation exponentielle très douce au début et à la fin"""
    if t == 0: 
        return 0.0
    if t == 1: 
        return 1.0
    if t < 0.5:
        return 0.5 * math.pow(2, (20 * t) - 10)
    else:
        return 1 - 0.5 * math.pow(2, -20 * t + 10)

def ease_in_quad(t: float) -> float:
    """Démarre doucement puis accélère"""
    return t * t

def ease_in_power(t: float, power: int = 4) -> float:
    """Interpolation très lente au début, violente à la fin"""
    return t**power

def ease_out_quad(t: float) -> float:
    """Accélère vite puis ralentit en douceur"""
    return 1 - (1 - t) * (1 - t)

def interpolate_colors(color1, color2, factor: float, easing_func=None) -> tuple[int, int, int, int]:
    """Interpole entre deux couleurs RGBA"""
    if easing_func:
        factor = easing_func(factor)
    r = int(color1[0] + (color2[0] - color1[0]) * factor)
    g = int(color1[1] + (color2[1] - color1[1]) * factor)
    b = int(color1[2] + (color2[2] - color1[2]) * factor)
    w = int(color1[3] + (color2[3] - color1[3]) * factor)
    return (r, g, b, w)

class ColorMode(ABC):
    @abstractmethod
    def get_color(self, note: int, velocity: int) -> tuple[int, int, int, int]:
        pass

class OneColor(ColorMode):
    def __init__(self, color=(255, 0, 0, 0)):
        self.color = color

    def get_color(self, note: int, velocity: int) -> tuple[int, int, int, int]:
        if self.color == (0, 0, 0, 0):
            log.warning("OneColor mode with color (0,0,0,0)")
        return self.color
    
    def set_color(self, color: tuple[int, int, int, int]):
        self.color = color
    
class Gradient(ColorMode):
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
    
class VelocityBased(ColorMode):
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