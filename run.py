import argparse
from src.config import get_default_config, OutputMode, Config
from src.controller import run_simulation


def parse_args():
    parser = argparse.ArgumentParser(description="Run City Simulation")
    parser.add_argument("--mode", type=str, choices=[m.value for m in OutputMode],
                        default="pygame", help="Output mode: pygame | json | none")
    parser.add_argument("--time", type=float, default=None,
                        help="Maximum simulation time (seconds). None = unlimited.")
    parser.add_argument("--fps", type=int, default=60, help="Frames per second")
    parser.add_argument("--walkers", type=int, default=1, help="Number of walkers")
    return parser.parse_args()


def main():
    args = parse_args()
    print(f"{args=}")
    cfg: Config = get_default_config()
    cfg.output_mode = OutputMode(args.mode)
    cfg.max_time = args.time
    cfg.fps = args.fps
    cfg.num_walkers = args.walkers

    run_simulation(cfg)


if __name__ == "__main__":
    main()
