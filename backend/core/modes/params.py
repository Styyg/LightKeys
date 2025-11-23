from typing import Any, Optional, List
from enum import Enum
from pydantic import BaseModel

# Tous les types de paramètres possibles côté métier
class ParamType(str, Enum):
    INT = "int",
    FLOAT = "float"
    BOOL = "bool"
    COLOR = "color"
    ENUM = "enum"
    LIST = "list"
    OBJECT = "object"
    STRING = "string"

class ParamDefinition(BaseModel):
    name: str                  # Nom interne (ex: "speed")
    label: str                 # Pour l'UI (ex: "Vitesse")
    type: ParamType            # ParamType.INT / FLOAT / LIST...
    default: Any               # Valeur par défaut
    min: Optional[float] = None
    max: Optional[float] = None
    options: Optional[List[str]] = None      # Pour ENUM
    item_schema: Optional["ParamDefinition"] = None  # Pour LIST
    fields: Optional[List["ParamDefinition"]] = None # Pour OBJECT

ParamDefinition.model_rebuild()
