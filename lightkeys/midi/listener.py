import time
import mido
import threading
import logging

log = logging.getLogger("MIDI")

MIDI_PORT_NAME = "USB MIDI Interface"

class MidiListener:
    """
    Classe qui écoute un périphérique MIDI en tâche de fond
    et envoie les événements (note_on/note_off) dans une queue.
    """

    def __init__(self, event_queue):
        self.event_queue = event_queue
        self.running = False
        input_ports = mido.get_input_names()
        for port in input_ports:
            if MIDI_PORT_NAME.upper() in port.upper():
                self.input_port = port
                break

    def _loop(self):
        """Boucle interne qui lit en continu le port MIDI"""
        with mido.open_input(self.input_port) as inport:
            while self.running:
                for msg in inport.iter_pending():
                    # On balance le message dans la queue
                    self.event_queue.put(msg)
                    match msg.type:
                        case "note_on" | "note_off":
                            pass
                            # log.debug(f"{msg.type.upper()}, NOTE={msg.note}, VELOCITY={msg.velocity}")
                        case "control_change":
                            pass
                            # log.debug(f"{msg.type.upper()}, CONTROL={msg.control}, VALUE={msg.value}")
                        case _:
                            log.debug("Event: " + str(msg))
                time.sleep(0.001)

    def start(self):
        """Lance l’écoute MIDI dans un thread séparé"""
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def stop(self):
        """Arrête l’écoute MIDI"""
        self.running = False
        if self.thread:
            self.thread.join()
        log.info("Listener stopped.")