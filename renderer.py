import queue
import time
from leds import LEDStrip, LED_COUNT
import logging

log = logging.getLogger("RENDERER")

FPS = 30  # images par seconde
LOWEST_MIDI_NOTE = 21
HIGHEST_MIDI_NOTE = 108

class Renderer:
    """
    Boucle qui lit les events MIDI et met à jour le bandeau LED
    """

    def __init__(self):
        self.queue = queue.Queue()   # queue partagée avec le MidiListener
        self.strip = LEDStrip()  # instance du bandeau
        self.running = False
        self.noteToLeds = {}  # mapping note → LED index
        self.initNotesToLeds()

    def initNotesToLeds(self):
        """Initialisation de la map de notes aux leds"""
        led_number = 0
        for note in range(LOWEST_MIDI_NOTE, HIGHEST_MIDI_NOTE + 1):
            match note:
                case 21 | 108:
                    self.noteToLeds[note] = {led_number, led_number + 1, led_number + 2}
                    led_number += 3
                case 56 | 93:
                    self.noteToLeds[note] = {led_number}
                    led_number += 1
                case _:
                    self.noteToLeds[note] = {led_number, led_number + 1}
                    led_number += 2
        # print("Note to LED mapping:", self.noteToLeds)

    def start(self):
        """Boucle principale du rendu"""
        self.running = True
        frame_time = 1.0 / FPS
        next_frame = time.monotonic()

        while self.running:
            while not self.queue.empty():
                msg = self.queue.get_nowait()
                led_indices = []
                if msg.type in ("note_on", "note_off"):
                    if msg.note < LOWEST_MIDI_NOTE or msg.note > HIGHEST_MIDI_NOTE:
                        log.warning(f"Note {msg.note} out of range ({LOWEST_MIDI_NOTE}-{HIGHEST_MIDI_NOTE})")
                        continue
                    led_indices = self.noteToLeds.get(msg.note, [])
                match msg.type:
                    case "note_on":
                        # On allume la LED correspondante en rouge
                        for led_index in led_indices:
                            self.strip.set_led(led_index, 255, 0, 0, 0)
                    case "note_off":
                        # On éteint la LED correspondante
                        for led_index in led_indices:
                            self.strip.set_led(led_index, 0, 0, 0, 0)
                    case "control_change":
                        pass
                        # log.debug(f"Control change: {msg.control}, {msg.value}")
                    case _:
                        log.warning(f"Unhandled event: {str(msg)}")

            # On rafraîchit le ruban à chaque frame
            now = time.monotonic()
            if now >= next_frame:
                self.strip.show()
                next_frame = now + frame_time

        time.sleep(0.001)

    def stop(self):
        """Arrêt propre du rendu"""
        self.running = False
        self.strip.clear()
        self.strip.show()
        log.info("Renderer stopped.")
