from dataclasses import dataclass
import os
from pathlib import Path
import json

@dataclass(frozen=True)
class AppConfig:
    db_uri: str
    dataseed_path: str
    seed_data: bool = True


def load_config(name: str = "local") -> AppConfig:
    """
    Loads configs/{name}.json
    """
    print("loading config...")
    
    root = Path(__file__).resolve().parents[2]
    config_path = root / "configs" / f"{name}.json"

    with open(config_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    load_data = os.getenv('LOAD_DATA', 'false').lower() == 'true'
    raw['seed_data'] = load_data

    config = AppConfig(**raw)

    print("config loaded")
    return config