import json
import os
from typing import Union
from src.types import Config

def load_config(filepath: str = "data/grid_config.json") -> Config:
    """Carga la configuración del grafo desde un archivo JSON."""
    if not os.path.exists(filepath):
        # Intentar ruta relativa al workspace por si se ejecuta desde subcarpetas
        filepath = os.path.join(os.path.dirname(__file__), "..", filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(config: Config, filepath: str = "data/grid_config.json") -> None:
    """Guarda la configuración del grafo en un archivo JSON."""
    if not os.path.isabs(filepath):
        filepath = os.path.join(os.path.dirname(__file__), "..", filepath)
        
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def format_time(minutes: Union[int, float]) -> str:
    """Formatea minutos flotantes en una cadena legible de minutos y segundos."""
    mins = int(minutes)
    secs = round((minutes - mins) * 60)
    if secs == 0: return f"{mins} min"
    return f"{mins} min {secs} seg"
