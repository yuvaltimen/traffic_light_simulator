import argparse
from src.config import get_default_config, OutputMode, Config
from src.controller import run_simulation


def parse_args():
    parser = argparse.ArgumentParser(description="Chickenville Pedestrian Simulation")
    parser.add_argument("--mode", type=str, choices=[m.value for m in OutputMode],
                        default="pygame", help="Output mode: pygame | json | statistics | none")
    parser.add_argument("--time", type=float, default=None,
                        help="Maximum simulation time (seconds). None = unlimited.")
    parser.add_argument("--screen_width", type=int, default=800, help="Screen width in pixels")
    parser.add_argument("--screen_height", type=int, default=600, help="Screen height in pixels")
    parser.add_argument("--frame_rate", type=int, default=60, help="Frame rate")

    parser.add_argument("--num_streets", type=int, default=5, help="Number of streets")
    parser.add_argument("--num_avenues", type=int, default=6, help="Number of avenues")
    parser.add_argument("--street_block_length", type=float, default=50.0, help="Street block length in meters")
    parser.add_argument("--street_crosswalk_length", type=float, default=20.0, help="Street crosswalk length in meters")
    parser.add_argument("--avenue_block_length", type=float, default=70.0, help="Avenue block length in meters")
    parser.add_argument("--avenue_crosswalk_length", type=float, default=40.0, help="Avenue crosswalk length in meters")

    parser.add_argument("--traffic_cycle", type=str, default="15.0,20.0", help="Comma separated pair of floats denoting traffic cycle times (ie. '20.0,30.0' denotes 20s green and 30s red)")
    parser.add_argument("--random_seed", type=int, default=42, help="Random seed for controlling simulation")

    parser.add_argument("--walker_speed", type=float, default=60.0, help="Walker speed in m/s")
    parser.add_argument("--walker_starting_corner", type=str, default="sw", choices=["nw", "sw", "ne", "se"], help="Street corner that the walker starts at")

    return parser.parse_args()


def main():
    args = parse_args()
    cfg: Config = get_default_config()
    cfg.output_mode = OutputMode(args.mode)
    cfg.screen_width = args.screen_width
    cfg.screen_height = args.screen_height
    cfg.frame_rate = args.frame_rate
    cfg.num_streets = args.num_streets
    cfg.num_avenues = args.num_avenues
    cfg.street_block_length = args.street_block_length
    cfg.street_crosswalk_length = args.street_crosswalk_length
    cfg.avenue_block_length = args.avenue_block_length
    cfg.avenue_crosswalk_length = args.avenue_crosswalk_length
    cfg.avenue_traffic_light_cycle_times = (float(args.traffic_cycle.split(",")[0]), float(args.traffic_cycle.split(",")[1]))
    cfg.random_seed = args.random_seed
    cfg.walker_speed = args.walker_speed
    cfg.walker_starting_corner = args.walker_starting_corner

    run_simulation(cfg)


if __name__ == "__main__":
    main()
