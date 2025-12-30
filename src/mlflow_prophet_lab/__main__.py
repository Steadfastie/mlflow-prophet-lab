from .config import load_config, AppConfig
from .data_loader import seed_data
from .holidays import get_holidays


def main() -> None:
    config = load_config()
    
    if config.seed_data:
        seed_data(config)
    else:
        print("Skipping data loading")


    holidays = get_holidays()
    print(holidays)


if __name__ == "__main__":
    main()