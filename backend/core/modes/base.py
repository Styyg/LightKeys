from abc import ABC, abstractmethod
from typing import List

from .params import ParamDef
from backend.core.modes.base import Mode
import logging

log = logging.getLogger("Modes")

class Mode(ABC):
    id: str
    name: str
    description: str

    @classmethod
    @abstractmethod
    def get_params_def(cls) -> List[ParamDef]:
        pass

class ColorMode(Mode):
    schema = {}

    @abstractmethod
    def get_color(self, msg: dict) -> tuple[int, int, int, int]:
        pass

    def update_params(self, params: dict):
        """Met à jour les paramètres du mode de couleur."""
        log.warning(f"update_params not implemented for {self.name}")

    def get_params(self) -> dict:
        """Retourne les paramètres du mode de couleur."""
        log.warning(f"get_params not implemented for {self.name}")
        return {}
    
class EffectMode(ABC):
    name = "Abstract EffectMode"
    description = "Abstract EffectMode Description"
    schema = {}

    def __init__(self):
        self.notes_to_render = {}

    @abstractmethod
    def apply(self, notes_state: dict, frame_note_events: list) -> list:
        pass

    def update_params(self, params: dict):
        """Met à jour les paramètres du mode d'effet."""
        log.warning(f"update_params not implemented for {self.name}")

    def get_params(self) -> dict:
        """Retourne les paramètres du mode d'effet."""
        log.warning(f"get_params not implemented for {self.name}")
        return {}

    def get_notes_to_render(self):
        return self.notes_to_render