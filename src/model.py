from dataclasses import dataclass
from typing import List, Optional, Tuple

# ------------------- State snapshots for the view -------------------
@dataclass(frozen=True)
class Location:
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

class CityGrid:
    def __init__(
        self,
        num_streets: int,
        num_avenues: int,
        street_block_length: float,
        street_crosswalk_length: float,
        avenue_block_length: float,
        avenue_crosswalk_length: float,
    ):
        self.num_streets = num_streets
        self.num_avenues = num_avenues

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

    # Walkers helpers (centerlines)
    def avenue_east(self, idx: int) -> float:
        return idx * self.avenue_spacing + self.avenue_block_length

    def avenue_west(self, idx: int) -> float:
        return idx * self.avenue_spacing + self.avenue_block_length + self.avenue_crosswalk_length

    def street_north(self, idx: int) -> float:
        return idx * self.street_spacing + self.street_block_length

    def street_south(self, idx: int) -> float:
        return idx * self.street_spacing + self.street_block_length + self.street_crosswalk_length

    def intersection_xy(self, street_idx: int, avenue_idx: int) -> Tuple[float, float]:
        return self.avenue_east(avenue_idx), self.street_north(street_idx)


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

class Walker:
    def __init__(self,
                 walker_id: str,
                 street_idx: int,
                 avenue_idx: int,
                 direction: str,
                 speed: float,
                 grid: CityGrid):
        self.id = walker_id
        self.street_idx = street_idx
        self.avenue_idx = avenue_idx
        self.direction = direction
        self.speed = speed
        self.grid = grid

        self.progress = 0.0  # 0..1 along current segment
        self._set_next_target()

    def _neighbor_indices(self, direction: str) -> Optional[Tuple[int, int]]:
        dj, di = _DIR_DELTA[direction]
        j, i = self.street_idx + dj, self.avenue_idx + di
        if 0 <= j < self.grid.num_streets and 0 <= i < self.grid.num_avenues:
            return j, i
        return None

    def _pick_next_direction(self, direction_dict: dict, start_dir: str) -> str:
        d = direction_dict[start_dir]
        for _ in range(4):
            if self._neighbor_indices(d) is not None:
                return d
            d = direction_dict[d]
        return start_dir

    def _set_next_target(self):
        nxt = self._neighbor_indices(self.direction)
        if nxt is None:
            self.direction = self._pick_next_direction(_ZIG_ZAG, self.direction)
            nxt = self._neighbor_indices(self.direction)
            if nxt is None:
                self.target = (self.street_idx, self.avenue_idx)
                return
        self.target = nxt
        self.progress = 0.0

    def update(self, dt: float):
        # Move along segment proportionally
        step = self.speed * dt / self.grid.avenue_spacing
        self.progress += step
        if self.progress >= 1.0:
            # Snap to intersection
            self.street_idx, self.avenue_idx = self.target
            self.direction = self._pick_next_direction(_ZIG_ZAG, self.direction)
            self._set_next_target()

    def to_state(self) -> WalkerState:
        j0, i0 = self.street_idx, self.avenue_idx
        j1, i1 = self.target

        x0, y0 = self.grid.intersection_xy(j0, i0)
        x1, y1 = self.grid.intersection_xy(j1, i1)
        x = x0 + (x1 - x0) * self.progress
        y = y0 + (y1 - y0) * self.progress
        return WalkerState(self.id, x, y, self.direction, j0, i0, j1, i1)


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
