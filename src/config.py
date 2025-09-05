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
    num_streets: int = 10
    num_avenues: int = 6
    street_block_length: float = 50.0
    street_crosswalk_length: float = 20.0
    avenue_block_length: float = 70.0
    avenue_crosswalk_length: float = 40.0

    # Agents
    walker_speed: float = 6.0
    walker_starting_direction: str = "north"
    walker_starting_corner: str = "nw"
    num_walkers: int = 1


    # Runtime
    fps: int = 60
    max_time: float | None = None  # None = run until quit, or set seconds


def get_default_config() -> Config:
    return Config()
