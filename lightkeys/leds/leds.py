from rpi_ws281x import PixelStrip, Color, ws
import logging

log = logging.getLogger("LEDS")

LED_COUNT      = 177     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_BRIGHTNESS = 100
LED_STRIP      = ws.SK6812_STRIP_GRBW

class LEDStrip:
    """
    Wrapper autour de rpi_ws281x pour simplifier l'utilisation du bandeau LED.
    """

    def __init__(self):
        # Création de l’objet PixelStrip
        self.strip = PixelStrip(
            LED_COUNT,
            LED_PIN,
            LED_FREQ_HZ,
            LED_DMA,
            LED_INVERT,
            LED_BRIGHTNESS,
            LED_CHANNEL,
            LED_STRIP
        )
        self.strip.begin()

    def set_led(self, index, color):
        """Définit la couleur d’une LED donnée (en RGB 0-255)."""
        if 0 <= index < LED_COUNT:
            log.debug(f"Led {index} to color {color}")
            self.strip.setPixelColor(index, Color(*color))
        else:
            log.warning(f"LED index {index} out of range (0-{LED_COUNT-1})")

    def clear(self):
        """Éteint toutes les LEDs (buffer seulement, pas encore envoyé)."""
        for i in range(LED_COUNT):
            self.strip.setPixelColor(i, Color(0, 0, 0, 0))

    def show(self):
        """Applique les changements sur le ruban."""
        self.strip.show()