import platform
from .color_modes import ColorMode
from .effect_modes import EffectMode
from .renderer import Renderer

if platform.machine().startswith("arm"):
    from .leds import LEDStrip
else:
    from .mock_strip import LEDStrip