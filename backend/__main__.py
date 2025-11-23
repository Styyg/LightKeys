import time
import logging
from .core.midi import MidiListener
from .core.renderer import Renderer
from .server import Server

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(name)s] - %(message)s',
    datefmt='%H:%M:%S',
)
log = logging.getLogger("MAIN")

def main():
    log.info("Démarrage de LightKeys...")
    renderer = Renderer()
    midi = MidiListener(renderer.queue)
    server = Server()
    server.set_renderer(renderer)

    try:
        midi.start()
        server.start()
        renderer.start()

        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        log.info("Interruption du programme...")
    except Exception as e:
        log.exception("Erreur inattendue: " + str(e))
    finally:
        log.info("Arrêt des services...")
        try:
            midi.stop()
        except Exception as e:
            log.warning(f"Erreur à l'arrêt du MIDI : {e}")
        try:
            renderer.stop()
        except Exception as e:
            log.warning(f"Erreur à l'arrêt du Renderer : {e}")
        try:
            server.stop()
        except Exception as e:
            log.warning(f"Erreur à l'arrêt du Server : {e}")

if __name__ == "__main__":
    main()
