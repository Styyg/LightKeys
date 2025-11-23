import pkgutil
import importlib
import inspect
from core.modes.base import Mode
from core.modes.color.base import ColorMode
from core.modes.effect.base import EffectMode

def load_modes_from_package(package_name: str):
    """Charge automatiquement toutes les classes Mode dans un package."""
    modes = []
    base_classes = {Mode, ColorMode, EffectMode}

    # Parcourt tous les modules du package
    package = importlib.import_module(package_name)

    for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        module_name = module_info.name

        module = importlib.import_module(module_name)

        # Inspecte le module → cherche des classes héritant de Mode
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Mode) and obj not in base_classes:
                modes.append(obj)

    return modes


# Charge les color modes et effect modes
COLOR_MODES = load_modes_from_package("core.modes.color")
EFFECT_MODES = load_modes_from_package("core.modes.effect")

# Liste complète
ALL_MODES = COLOR_MODES + EFFECT_MODES
