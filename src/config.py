from dataclasses import dataclass
from enum import Enum


class OutputMode(str, Enum):
    JSON = "json"
    PYGAME = "pygame"
    NONE = "none"   # headless (model only, no output)


@dataclass
class Config:
    # Visualization
    output_mode: OutputMode = OutputMode.PYGAME
    screen_width: int = 800
    screen_height: int = 800
    frame_rate: int = 60

    # Simulation world
    num_streets: int = 3
    num_avenues: int = 2
    street_block_length: float = 50.0
    street_crosswalk_length: float = 20.0
    avenue_block_length: float = 70.0
    avenue_crosswalk_length: float = 40.0

    # tuple representing the (green, red) light times to cross the avenue
    # the corresponding traffic light times is the reverse, ie. (red, green)
    avenue_traffic_light_cycle_times: float = (15.0, 20.0)
    traffic_light_grid_random_seed: int = 42

    # Agents
    walker_speed: float = 50.0
    walker_starting_direction: str = "north"
    walker_starting_corner: str = "nw"
    num_walkers: int = 1


    # Runtime
    fps: int = 60
    max_time: float | None = None  # None = run until quit, or set seconds


def get_default_config() -> Config:
    return Config()
