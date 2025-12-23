from dataclasses import dataclass
from pathlib import Path
import json

@dataclass(frozen=True)
class AppConfig:
    db_uri: str


def load_config(name: str = "local") -> AppConfig:
    """
    Loads configs/{name}.json
    """
    root = Path(__file__).resolve().parents[2]
    config_path = root / "configs" / f"{name}.json"

    with open(config_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    return AppConfig(**raw)