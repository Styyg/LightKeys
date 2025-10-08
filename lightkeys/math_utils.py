import math

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