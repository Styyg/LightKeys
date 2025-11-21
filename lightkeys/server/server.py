import threading
import uvicorn
import logging
from . import api

log = logging.getLogger("SERVER")

class Server:
    def __init__(self, host: str = "0.0.0.0", port: int = 8080):
        self.host = host
        self.port = port
        self.thread = None
        self.running = False

    def set_renderer(self, renderer):
        """Associe un renderer au serveur."""
        api.set_renderer(renderer)
        
    def start(self):
        """Démarre le serveur FastAPI dans un thread séparé."""
        if self.running:
            log.warning("Le serveur est déjà démarré.")
            return
        
        log.info("Démarrage du serveur API...")
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
    
    def _run(self):
        log.debug(f"Lancement d'uvicorn sur {self.host}:{self.port}")
        uvicorn.run(api.app, host=self.host, port=self.port)

    def stop(self):
        """(Optionnel pour plus tard) Arrête proprement le serveur."""
        log.info("Arrêt du serveur (non implémenté proprement encore).")
        self.running = False
        # FastAPI/Uvicorn ne permet pas un stop simple via API sans hack,
        # donc on laisse le thread daemon se fermer avec le programme.