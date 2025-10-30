import queue
import time
import logging
import inspect
from .leds import color_modes, effect_modes, LEDStrip

log = logging.getLogger("RENDERER")

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
        self.effectsMode = []
        self.FPS = 60
        
        self.load_color_mode_list()
        self.load_effect_mode_list()

        # Modes par défaut
        self.set_color_mode(color_modes.OneColor.name)
        self.add_effect_mode(effect_modes.NoteOnEffect())
        self.add_effect_mode(effect_modes.FadeOutEffect(0.15))

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
        self.check_modes()
        self.running = True
        frame_time = 1.0 / self.FPS
        next_frame = time.monotonic()
        note_events_this_frame = []

        while self.running:
            while not self.queue.empty():
                msg = self.queue.get_nowait()
                if msg.type in ("note_on", "note_off"):
                    if msg.note < LOWEST_MIDI_NOTE or msg.note > HIGHEST_MIDI_NOTE:
                        log.warning(f"Note {msg.note} out of range ({LOWEST_MIDI_NOTE}-{HIGHEST_MIDI_NOTE})")
                        continue

                if self.colorMode is None:
                    log.error("No color mode set, cannot process MIDI events.")
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

    def check_modes(self):
        if self.colorMode is None:
            log.warning("No color mode set.")
        if not self.effectsMode:
            log.warning("No effect modes set.")

    # def set_color_mode(self, mode: color_modes.ColorMode):
    #     """Change le mode de couleur"""
    #     self.colorMode = mode
    #     log.info(f"Color mode changed to: {type(mode).__name__}")

    def add_effect_mode(self, mode: effect_modes.EffectMode):
        """Ajoute un mode d'effet (en plus de l'actuel)"""
        self.effectsMode.append(mode)
        log.debug(f"Effect mode added: {type(mode).__name__}")

    def load_color_mode_list(self):
        """Charge la liste des modes de couleur disponibles"""
        self.colorModeList = {}
        for name, obj in inspect.getmembers(color_modes, inspect.isclass):
            if issubclass(obj, color_modes.ColorMode) and obj is not color_modes.ColorMode:
                instance = obj()
                self.colorModeList[instance.name] = instance

    def load_effect_mode_list(self):
        """Charge la liste des modes d'effet disponibles"""
        self.effectModeList = {}
        for name, obj in inspect.getmembers(effect_modes, inspect.isclass):
            if issubclass(obj, effect_modes.EffectMode) and obj is not effect_modes.EffectMode:
                instance = obj()
                self.effectModeList[instance.name] = instance

    def list_color_modes(self):        
        """Retourne la liste des modes de couleur disponibles"""
        return list(self.colorModeList.keys())

    def list_effect_modes(self):
        """Retourne la liste des modes d'effet disponibles"""
        return list(self.effectModeList.keys())
    
    def set_color_mode(self, name: str):
        """Change le mode actif."""
        if name not in self.colorModeList:
            raise ValueError(f"Color mode inconnu : {name}")
        self.colorMode = self.colorModeList[name]        
        log.debug(f"Color mode changed to: {name}")

    def get_active_color_mode(self):
        """Nom du mode actif."""
        if not self.colorMode:
            return None
        return self.colorMode.name
    
    def get_active_effect_modes(self):
        """Noms des modes d'effet actifs."""
        active_effects = {}
        for effect in self.effectsMode:
            if effect is None:
                continue
            active_effects[effect.name] = effect.get_params()
    
    def set_color_params(self, params: dict):
        """Met à jour les paramètres du mode actif."""
        if not self.colorMode:
            raise RuntimeError("Aucun mode actif")
        self.colorMode.update_params(params)

    def get_color_params(self):
        """Retourne les paramètres du mode actif."""
        if not self.colorMode:
            return {}
        return self.colorMode.get_params()
    
    def set_effect_params(self, effect_id, params: dict):
        if(len(self.effectsMode) <= effect_id or self.effectsMode[effect_id] is None):
            raise ValueError(f"Effect ID {effect_id} out of range")
        self.effectsMode[effect_id].update_params(params)

    def list_mode_schemas(self):
        """Retourne la description et le schéma de chaque mode."""
        schemas = {"color_modes": {}, "effect_modes": {}}

        for name, instance in self.colorModeList.items():
            schemas["color_modes"][name] = {
                "description": getattr(instance, "description", ""),
                "params": getattr(instance, "schema", {})
            }

        for name, instance in self.effectModeList.items():
            schemas["effect_modes"][name] = {
                "description": getattr(instance, "description", ""),
                "params": getattr(instance, "schema", {})
            }

        return schemas
