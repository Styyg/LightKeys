import queue
import time
import logging
import color_modes, effect_modes
from leds import LEDStrip

log = logging.getLogger("RENDERER")

FPS = 60  # images par seconde
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
        self.notes_state = {}
        self.colorMode = None
        self.effectMode = None
        self.effectsMode = []
        
        # self.set_color_mode(color_modes.OneColor((255,0,0,0)))

        # dictionary = {21: (255, 0, 0, 0), 
        #              108: (255, 255, 255, 0)
        #              }
        # gradient = color_modes.Gradient(dictionary)
        # self.set_color_mode(gradient)

        self.set_color_mode(color_modes.VelocityBased((255,0,0,0), (0,0,0,255), 40, 100, color_modes.ease_in_power))

        self.add_effect_mode(effect_modes.NoteOnEffect())
        self.add_effect_mode(effect_modes.FadeOutEffect(0.2))

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

    def start(self):
        """Boucle principale du rendu"""
        self.running = True
        frame_time = 1.0 / FPS
        next_frame = time.monotonic()
        note_events_this_frame = []

        while self.running:
            while not self.queue.empty():
                msg = self.queue.get_nowait()
                if msg.type in ("note_on", "note_off"):
                    if msg.note < LOWEST_MIDI_NOTE or msg.note > HIGHEST_MIDI_NOTE:
                        log.warning(f"Note {msg.note} out of range ({LOWEST_MIDI_NOTE}-{HIGHEST_MIDI_NOTE})")
                        continue

                match msg.type:
                    case "note_on":
                        color = self.colorMode.get_color(msg.note, msg.velocity)

                        if msg.note not in self.notes_state:
                            self.notes_state[msg.note] = {}
                        self.notes_state[msg.note].update({
                            "state": 1,
                            "velocity": msg.velocity,
                            "start_time": time.monotonic(),
                            "color": color
                        })
                        note_events_this_frame.append(msg.note)
                        
                    case "note_off":                        
                        if msg.note not in self.notes_state:
                            self.notes_state[msg.note] = {}
                        self.notes_state[msg.note].update({
                            "state": 0,
                            "velocity": msg.velocity,
                            "start_time": time.monotonic()
                        })
                        note_events_this_frame.append(msg.note)

                    case "control_change":
                        pass
                    case _:
                        log.warning(f"Unhandled event: {str(msg)}")


            # On rafraîchit le ruban à chaque frame
            now = time.monotonic()
            if now >= next_frame:
                self.render_effects(note_events_this_frame)
                note_events_this_frame.clear()
                self.strip.show()
                next_frame = now + frame_time

        time.sleep(0.001)

    def render_effects(self, note_events):
        # self.effectMode.apply(self.notes_state)
        notes_to_render = {}        
        for effect in self.effectsMode:
            effect.apply(self.notes_state, note_events)
            notes_to_render.update(effect.get_notes_to_render())

        for note, color in notes_to_render.items():
            led_indices = self.noteToLeds.get(note, [])
            for led_index in led_indices:
                self.strip.set_led(led_index, color)

    def stop(self):
        """Arrêt propre du rendu"""
        self.running = False
        self.strip.clear()
        self.strip.show()
        log.info("Renderer stopped.")

    def set_color_mode(self, mode: color_modes.ColorMode):
        """Change le mode de couleur"""
        self.colorMode = mode
        log.info(f"Color mode changed to {type(mode).__name__}")

    def add_effect_mode(self, mode: effect_modes.EffectMode):
        """Ajoute un mode d'effet (en plus de l'actuel)"""
        self.effectsMode.append(mode)
        log.info(f"Effect mode added: {type(mode).__name__}")
