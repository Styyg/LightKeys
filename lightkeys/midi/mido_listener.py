from .listener import BaseListener
import mido
import time
import threading
import logging

log = logging.getLogger("MIDI")

class MidoListener(BaseListener):
    """
    Classe qui écoute un périphérique MIDI en tâche de fond
    et envoie les événements (note_on/note_off) dans une queue.
    """
    MIDI_PORT_NAME = "USB MIDI Interface"

    def __init__(self, event_queue):
        self.event_queue = event_queue
        self.running = False
        self.input_port = None
        input_ports = mido.get_input_names()
        for port in input_ports:
            if self.MIDI_PORT_NAME.upper() in port.upper():
                self.input_port = port
                break
        if(self.input_port == None):
            log.warning("No midi input port found")

    def _loop(self):
        """Boucle interne qui lit en continu le port MIDI"""
        with mido.open_input(self.input_port) as inport:
            while self.running:
                for msg in inport.iter_pending():
                    # On balance le message dans la queue
                    self.event_queue.put(msg)
                    match msg.type:
                        case "note_on" | "note_off":
                            # log.debug(f"{msg.type.upper()}, NOTE={msg.note}, VELOCITY={msg.velocity}")
                            pass
                        case "control_change":
                            # log.debug(f"{msg.type.upper()}, CONTROL={msg.control}, VALUE={msg.value}")
                            pass
                        case _:
                            log.debug("Event: " + str(msg))
                time.sleep(0.001)

    def start(self):
        """Lance l’écoute MIDI dans un thread séparé"""
        if(self.input_port == None):
            log.error("No midi input port assigned.")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def stop(self):
        """Arrête l’écoute MIDI"""
        if(self.running == False):
            log.warning("Midi Listener already stopped.")
            return
        
        self.running = False
        if self.thread:
            self.thread.join()
        log.info("Listener stopped.")