import os
from .config import load_config, AppConfig
from .data_loader import seed_data


def main() -> None:
    config = load_config()
    
    if config.seed_data:
        seed_data(config)
    else:
        print("Skipping data loading")


if __name__ == "__main__":
    main()