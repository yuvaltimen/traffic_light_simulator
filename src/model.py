from dataclasses import dataclass
import random
from typing import List, Optional, Tuple

# ------------------- State snapshots for the view -------------------
@dataclass(frozen=True)
class StreetCornerLocation:
    street_idx: int
    avenue_idx: int
    corner: str  # "east", "south", "west", "north"

@dataclass(frozen=True)
class WalkerState:
    id: str
    x: float
    y: float
    direction: str  # "east", "south", "west", "north"
    current_street_idx: int
    current_avenue_idx: int
    target_street_idx: int
    target_avenue_idx: int

@dataclass(frozen=True)
class SimulationState:
    time: float
    walkers: List[WalkerState]


# ------------------- City Grid -------------------

def create_traffic_light_grid(num_streets: int, num_avenues: int, cycle_length: float, rndm_seed: int) -> dict[tuple[int, int], float]:
    """
    Creates the offset grid for the traffic light cycles.
    :param num_avenues: number of avenues in the simulation
    :param num_streets: number of streets in the simulation
    :param cycle_length: total length of the green + red time in seconds
    :param rndm_seed: random number generator seed to use
    :return: Dictionary
        keys: tuple(int, int), representing (avenue_index, street_index) intersection
        values: float, representing the number of seconds the given intersection's
            traffic light initial offset is in its cycle, (ie. 1.2s means when the simulation
            starts, this intersection will begin 1.2s into its cycle)
    """
    random.seed(rndm_seed)
    d = dict()
    for x in range(num_avenues):
        for y in range(num_streets):
            d[(x,y)] = random.random() * cycle_length
    return d


class CityGrid:
    def __init__(
        self,
        num_streets: int,
        num_avenues: int,
        street_block_length: float,
        street_crosswalk_length: float,
        avenue_block_length: float,
        avenue_crosswalk_length: float,
        avenue_traffic_light_cycle_times: tuple[float, float],
        traffic_light_grid_random_seed: int,
    ):
        # city size
        self.num_streets = num_streets
        self.num_avenues = num_avenues

        # street lengths
        self.street_block_length = street_block_length
        self.street_crosswalk_length = street_crosswalk_length
        self.avenue_block_length = avenue_block_length
        self.avenue_crosswalk_length = avenue_crosswalk_length

        # spacing for moving along grid
        self.street_spacing = street_block_length + street_crosswalk_length
        self.avenue_spacing = avenue_block_length + avenue_crosswalk_length

        # total dimensions
        self.width = num_avenues * self.avenue_spacing + avenue_block_length
        self.height = num_streets * self.street_spacing + street_block_length

        # traffic lights
        self.avenue_traffic_light_cycle_times = avenue_traffic_light_cycle_times
        self.traffic_light_cycle_length = self.avenue_traffic_light_cycle_times[0] + self.avenue_traffic_light_cycle_times[1]
        self.traffic_light_grid_random_seed = traffic_light_grid_random_seed
        self.traffic_light_grid = create_traffic_light_grid(
            self.num_streets,
            self.num_avenues,
            self.traffic_light_cycle_length,
            self.traffic_light_grid_random_seed,
        )

    # Drawing helpers (edges of crosswalks)
    def avenue_positions(self):
        for i in range(self.num_avenues):
            left = i * self.avenue_spacing + self.avenue_block_length
            right = left + self.avenue_crosswalk_length
            yield left, right

    def street_positions(self):
        for j in range(self.num_streets):
            top = j * self.street_spacing + self.street_block_length
            bottom = top + self.street_crosswalk_length
            yield top, bottom

    def avenue_east(self, idx: int) -> float:
        return idx * self.avenue_spacing + self.avenue_block_length

    def avenue_west(self, idx: int) -> float:
        return idx * self.avenue_spacing + self.avenue_block_length + self.avenue_crosswalk_length

    def street_north(self, idx: int) -> float:
        return idx * self.street_spacing + self.street_block_length

    def street_south(self, idx: int) -> float:
        return idx * self.street_spacing + self.street_block_length + self.street_crosswalk_length

    def intersection_xy(self, avenue_idx: int, street_idx: int, ) -> Tuple[float, float]:
        return self.avenue_east(avenue_idx) + (self.avenue_crosswalk_length / 2), self.street_north(street_idx) + (self.street_crosswalk_length / 2)

    def corner_xy(self, street_idx: int, avenue_idx: int, corner: str):
        left, right = list(self.avenue_positions())[avenue_idx]
        top, bottom = list(self.street_positions())[street_idx]

        if corner == "nw":
            return left, bottom
        elif corner == "ne":
            return right, bottom
        elif corner == "sw":
            return left, top
        elif corner == "se":
            return right, top
        return None


# ------------------- Walker -------------------

_RIGHT_TURN = {
    "east": "south",
    "south": "west",
    "west": "north",
    "north": "east",
}

_ZIG_ZAG = {
    "east": "south",
    "south": "east"
}

_DIR_DELTA = {
    "east":  (0, +1),
    "west":  (0, -1),
    "south": (+1, 0),
    "north": (-1, 0),
}

_CORNER_DELTAS = {
    # corner -> list of neighbor corner moves (dj, di, new_corner)
    "nw": {  # northwest
        "east": (0, 0, "ne"),   # east along crosswalk to same intersection
        "north": (+1, 0, "sw"),  # north along avenue
        "west": (0, -1, "ne"),  # west along street
        "south": (0, 0, "sw"),   # south along crosswalk to same intersection
    },
    "ne": {
        "north": (+1, 0, "se"),  # north along avenue
        "east": (0, +1, "nw"),  # east along street
        "west": (0, 0, "nw"),  # west along crosswalk to same intersection
        "south": (0, 0, "se"),  # south along crosswalk to same intersection
    },
    "sw": {
        "north": (0, 0, "nw"),  # north along crosswalk to same intersection
        "east": (0, 0, "se"),  # east along crosswalk to same intersection
        "west": (0, -1, "se"),  # west along street
        "south": (-1, 0, "nw"),  # south along avenue
    },
    "se": {
        "north": (0, 0, "ne"),  # north along crosswalk to same intersection
        "east": (0, +1, "sw"),  # east along street
        "south": (-1, 0, "ne"),  # south along avenue
        "west": (0, 0, "sw"),  # west along crosswalk to same intersection
    }
}
class Walker:
    def __init__(self,
                 walker_id: str,
                 street_idx: int,
                 avenue_idx: int,
                 corner: str,
                 direction: str,
                 speed: float,
                 target: StreetCornerLocation,
                 grid: CityGrid):
        self.id = walker_id
        self.street_idx = street_idx
        self.avenue_idx = avenue_idx
        self.corner = corner  # "nw", "ne", "sw", "se"
        self.direction = direction
        self.speed = speed
        self.grid = grid
        self.progress = 0.0
        self.target = target
        self._set_next_target()

    def _neighbor(self) -> Optional[Tuple[int, int, str]]:
        """Return the next corner and its indices along current direction"""
        for dj, di, new_corner in _CORNER_DELTAS[self.corner].values():
            j = self.street_idx + dj
            i = self.avenue_idx + di
            if 0 <= j < self.grid.num_streets and 0 <= i < self.grid.num_avenues:
                return j, i, new_corner
        return None

    def _set_next_target(self):
        nxt = self._neighbor()
        if nxt is None:
            # Stay in place if no neighbor
            self.target = (self.street_idx, self.avenue_idx, self.corner)
        else:
            self.target = nxt
        self.progress = 0.0

    def update(self, dt: float):
        step = self.speed * dt / max(self.grid.street_spacing, self.grid.avenue_spacing)
        self.progress += step
        if self.progress >= 1.0:
            # Snap to target corner
            self.street_idx, self.avenue_idx, self.corner = self.target
            self._set_next_target()

    def to_state(self):
        j0, i0, c0 = self.street_idx, self.avenue_idx, self.corner
        j1, i1, c1 = self.target
        x0, y0 = self.grid.corner_xy(j0, i0, c0)
        x1, y1 = self.grid.corner_xy(j1, i1, c1)
        x = x0 + (x1 - x0) * self.progress
        y = y0 + (y1 - y0) * self.progress
        return {
            "id": self.id,
            "x": x,
            "y": y,
            "corner": self.corner,
            "direction": self.direction,
            "start": (j0, i0, c0),
            "end": (j1, i1, c1)
        }


# ------------------- Simulation -------------------

class CitySimulation:
    def __init__(self, grid: CityGrid, walkers: List[Walker]):
        self.grid = grid
        self.walkers = walkers
        self.time: float = 0.0

    def step(self, dt: float) -> SimulationState:
        self.time += dt
        for w in self.walkers:
            w.update(dt)
        return SimulationState(
            time=self.time,
            walkers=[w.to_state() for w in self.walkers],
        )
