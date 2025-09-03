from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class WalkerState:
    id: int
    x: float
    y: float
    direction: Tuple[int, int]


@dataclass
class SimulationState:
    time: float
    walkers: List[WalkerState]


class CityGrid:
    """City definition in world units (e.g., meters)."""

    def __init__(self, num_streets, num_avenues,
                 street_block_length, street_crosswalk_length,
                 avenue_block_length, avenue_crosswalk_length):
        self.num_streets = num_streets
        self.num_avenues = num_avenues
        self.street_block_length = street_block_length
        self.street_crosswalk_length = street_crosswalk_length
        self.avenue_block_length = avenue_block_length
        self.avenue_crosswalk_length = avenue_crosswalk_length

        self.width = (num_avenues + 1) * avenue_block_length + num_avenues * avenue_crosswalk_length
        self.height = (num_streets + 1) * street_block_length + num_streets * street_crosswalk_length

    def avenue_positions(self):
        """Return x coordinates (world units) of avenue lines (pairs left/right)."""
        positions = []
        for i in range(self.num_avenues):
            left = self.avenue_block_length + i * (self.avenue_block_length + self.avenue_crosswalk_length)
            right = left + self.avenue_crosswalk_length
            positions.append((left, right))
        return positions

    def street_positions(self):
        """Return y coordinates (world units) of street lines (pairs top/bottom)."""
        positions = []
        for i in range(self.num_streets):
            top = self.street_block_length + i * (self.street_block_length + self.street_crosswalk_length)
            bottom = top + self.street_crosswalk_length
            positions.append((top, bottom))
        return positions


class Walker:
    """An agent moving along the grid in world units."""

    def __init__(self, id, start_x, start_y, speed, grid: CityGrid):
        self.id = id
        self.x = start_x
        self.y = start_y
        self.speed = speed  # world units per second
        self.dx, self.dy = 1, 0  # start moving east
        self.grid = grid

    def update(self, dt):
        self.x += self.dx * self.speed * dt
        self.y += self.dy * self.speed * dt

        # Simple bounce behavior: zigzag east/south
        if self.dx != 0:  # moving along avenue
            if self.x >= self.grid.width or self.x <= 0:
                self.x = max(0, min(self.x, self.grid.width))
                self.dx, self.dy = 0, 1  # turn south
        elif self.dy != 0:  # moving along street
            if self.y >= self.grid.height or self.y <= 0:
                self.y = max(0, min(self.y, self.grid.height))
                self.dx, self.dy = 1, 0  # turn east

    def to_state(self) -> WalkerState:
        return WalkerState(self.id, self.x, self.y, (self.dx, self.dy))


class CitySimulation:
    """Encapsulates the simulation model."""

    def __init__(self, grid: CityGrid, walkers: List[Walker]):
        self.grid = grid
        self.walkers = walkers
        self.time = 0.0

    def step(self, dt: float) -> SimulationState:
        self.time += dt
        for w in self.walkers:
            w.update(dt)
        return SimulationState(
            time=self.time,
            walkers=[w.to_state() for w in self.walkers]
        )
