from dataclasses import dataclass
from typing import List, Tuple, Optional


# --------- Public immutable state snapshots (what the View consumes) ---------

@dataclass(frozen=True)
class WalkerState:
    id: int
    x: float
    y: float
    direction: str  # "east" | "south" | "west" | "north"


@dataclass(frozen=True)
class SimulationState:
    time: float
    walkers: List[WalkerState]


# ------------------------------ City grid model ------------------------------

class CityGrid:
    """
    Grid in world units (e.g., meters). We model a repeating pattern:
      [block][crosswalk][block][crosswalk]... [block]
    along both X (avenues) and Y (streets).

    There are:
      - num_avenues vertical centerlines (crosswalk centers) indexed [0..num_avenues-1]
      - num_streets  horizontal centerlines (crosswalk centers) indexed [0..num_streets-1]
    """

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

        # Keep the atomic pieces for precise center calculations
        self.street_block_length = street_block_length
        self.street_crosswalk_length = street_crosswalk_length
        self.avenue_block_length = avenue_block_length
        self.avenue_crosswalk_length = avenue_crosswalk_length

        # Distance between consecutive street centerlines (top->bottom)
        self.street_spacing = street_block_length + street_crosswalk_length
        # Distance between consecutive avenue centerlines (left->right)
        self.avenue_spacing = avenue_block_length + avenue_crosswalk_length

        # Full extents (include a block on both ends)
        self.width = (num_avenues + 1) * avenue_block_length + num_avenues * avenue_crosswalk_length
        self.height = (num_streets + 1) * street_block_length + num_streets * street_crosswalk_length

    # ---- Crosswalk centerlines (what we draw and what walkers follow) ----

    def avenue_center_x(self, i: int) -> float:
        """X position of avenue centerline i (vertical line that pedestrians walk along)."""
        # start at left margin block, then go i spacings, then center of crosswalk
        left_of_crosswalk = self.avenue_block_length + i * (self.avenue_block_length + self.avenue_crosswalk_length)
        return left_of_crosswalk + 0.5 * self.avenue_crosswalk_length

    def street_center_y(self, j: int) -> float:
        """Y position of street centerline j (horizontal line that pedestrians walk along)."""
        top_of_crosswalk = self.street_block_length + j * (self.street_block_length + self.street_crosswalk_length)
        return top_of_crosswalk + 0.5 * self.street_crosswalk_length

    def avenue_centerlines(self):
        """Yield all avenue centerline X positions, left → right."""
        for i in range(self.num_avenues):
            yield self.avenue_center_x(i)

    def street_centerlines(self):
        """Yield all street centerline Y positions, top → bottom."""
        for j in range(self.num_streets):
            yield self.street_center_y(j)

    def intersection_xy(self, street_idx: int, avenue_idx: int) -> Tuple[float, float]:
        """World coords for the intersection of street j and avenue i (centerlines cross)."""
        return self.avenue_center_x(avenue_idx), self.street_center_y(street_idx)


# ------------------------------ Walker (agent) -------------------------------

_RIGHT_TURN = {
    "east": "south",
    "south": "west",
    "west": "north",
    "north": "east",
}

# Movement deltas for indices when committing a segment
_DIR_DELTA = {
    "east":  (0, +1),  # (d_street_idx, d_avenue_idx)
    "west":  (0, -1),
    "south": (+1, 0),
    "north": (-1, 0),
}


class Walker:
    """
    Walker constrained to *centerlines* only. It always traverses from one
    intersection center to an adjacent one, then turns (right by default)
    at every corner. If the 'right turn' would go out of bounds, it rotates
    right until a valid next segment exists (max 3 tries).
    """

    def __init__(
        self,
        id: int,
        street_idx: int,
        avenue_idx: int,
        direction: str,   # "east" | "south" | "west" | "north"
        speed: float,     # world units per second
        grid: CityGrid,
    ):
        self.id = id
        self.street_idx = street_idx
        self.avenue_idx = avenue_idx
        self.direction = direction
        self.speed = speed
        self.grid = grid

        # current segment: from (i0,j0) to (i1,j1), with progress s in [0, L]
        self._from = (self.street_idx, self.avenue_idx)
        self._to: Optional[Tuple[int, int]] = None
        self._seg_len: float = 0.0  # world length of current segment
        self._s: float = 0.0        # distance traveled along current segment

        # initialize a valid first segment
        self._start_new_segment_if_needed()

    # ---- public API used by simulation ----

    def update(self, dt: float) -> None:
        """Advance by dt seconds along centerlines, turning at corners."""
        remaining = self.speed * dt
        while remaining > 0.0:
            if self._to is None or self._seg_len <= 0.0:
                self._start_new_segment_if_needed()
                # if still None (degenerate 1x1 grid), break to avoid div-by-zero
                if self._to is None or self._seg_len <= 0.0:
                    return

            step = min(remaining, self._seg_len - self._s)
            self._s += step
            remaining -= step

            # reached the corner: commit and choose next segment
            if self._s >= self._seg_len - 1e-9:
                self.street_idx, self.avenue_idx = self._to
                self._from = (self.street_idx, self.avenue_idx)
                self._s = 0.0
                # alternate direction (turn right); adjust if out of bounds
                self.direction = self._pick_next_direction(self.direction)
                self._start_new_segment_if_needed()

    def to_state(self) -> WalkerState:
        x, y = self._current_xy()
        return WalkerState(self.id, x, y, self.direction)

    # ---- helpers ----

    def _segment_length_for_direction(self, direction: str) -> float:
        if direction in ("east", "west"):
            return self.grid.avenue_spacing
        else:
            return self.grid.street_spacing

    def _neighbor_indices(self, direction: str) -> Optional[Tuple[int, int]]:
        dj, di = _DIR_DELTA[direction]
        j = self.street_idx + dj
        i = self.avenue_idx + di
        if 0 <= j < self.grid.num_streets and 0 <= i < self.grid.num_avenues:
            return (j, i)
        return None

    def _pick_next_direction(self, start_direction: str) -> str:
        """
        Turn right; if that would leave the grid from current (j,i), rotate right
        up to 3 times until a valid neighbor exists.
        """
        d = _RIGHT_TURN[start_direction]
        for _ in range(4):  # try up to 4 directions
            if self._neighbor_indices(d) is not None:
                return d
            d = _RIGHT_TURN[d]
        # fallback: keep current direction if everything else fails
        return start_direction

    def _start_new_segment_if_needed(self) -> None:
        """Ensure we have a valid _to and segment length for current direction."""
        nxt = self._neighbor_indices(self.direction)
        if nxt is None:
            # rotate right until valid
            self.direction = self._pick_next_direction(self.direction)
            nxt = self._neighbor_indices(self.direction)
            if nxt is None:
                self._to = None
                self._seg_len = 0.0
                return
        self._to = nxt
        self._seg_len = self._segment_length_for_direction(self.direction)
        self._s = min(self._s, self._seg_len)  # clamp just in case

    def _current_xy(self) -> Tuple[float, float]:
        """World coordinates interpolated along the current segment."""
        j0, i0 = self._from
        if self._to is None or self._seg_len <= 0.0:
            # just sit at the intersection
            return self.grid.intersection_xy(j0, i0)

        j1, i1 = self._to
        x0, y0 = self.grid.intersection_xy(j0, i0)
        x1, y1 = self.grid.intersection_xy(j1, i1)
        t = self._s / self._seg_len if self._seg_len > 0 else 0.0
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t
        return x, y


# ---------------------------- Simulation container ---------------------------

class CitySimulation:
    """Advances walkers and produces immutable snapshots for the View."""

    def __init__(self, grid: CityGrid, walkers: List[Walker]):
        self.grid = grid
        self.walkers = walkers
        self.time: float = 0.0

    def step(self, dt: float) -> SimulationState:
        self.time += dt
        for w in self.walkers:
            w.update(dt)
        # IMPORTANT: return WalkerState objects (what the View expects)
        return SimulationState(
            time=self.time,
            walkers=[w.to_state() for w in self.walkers],
        )
