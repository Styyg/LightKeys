from pydantic import BaseModel
from typing import Dict, Any, Optional, List

class ModeInput(BaseModel):
    mode: str

class ParamsInput(BaseModel):
    params: Dict[str, Any]

class ParamsDefinition(BaseModel):
    name: str
    label: str
    type: str
    min: Optional[float] = None
    max: Optional[float] = None
    options: Optional[List[str]] = None
    item_schema: Optional[Dict[str, Any]] = None   # pour les listes

class Mode(BaseModel):
    id: str
    name: str
    params_schema: List[ParamsDefinition]
    params: Dict[str, Any]