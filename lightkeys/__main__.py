import time
import logging
from .midi import MidiListener
from .leds import Renderer

logging.basicConfig(
    # level=logging.INFO,
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(name)s] - %(message)s',
    datefmt='%H:%M:%S'
)
log = logging.getLogger("MAIN")

def main():
    log.info("Démarrage de LightKeys...")
    renderer = Renderer()
    midi = MidiListener(renderer.queue)

    try:
        midi.start()
        renderer.start()

        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        log.info("Interruption du programme...")
    except Exception as e:
        log.exception("Erreur inattendue: " + str(e))
    finally:
        log.info("Arrêt des services...")
        midi.stop()
        renderer.stop()

if __name__ == "__main__":
    main()
