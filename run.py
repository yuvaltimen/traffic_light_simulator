from src.config import get_default_config, Config
from src.controller import run_simulation


def main():
    cfg: Config = get_default_config()
    run_simulation(cfg)


if __name__ == "__main__":
    main()
