import platform
if platform.machine().startswith("arm"):
    from .hardware_strip import HardwareStrip
    LEDStrip = HardwareStrip
else:
    from .strip import MockStrip
    LEDStrip = MockStrip