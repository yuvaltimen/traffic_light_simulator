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
    walkers: List[dict]


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
    if rndm_seed:
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
        traffic_light_grid_random_seed: int = None,
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
        "north": (+1, 0, "sw"),  # north along avenue
        "east": (0, 0, "ne"),   # east along crosswalk to same intersection
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
        "west": (0, 0, "sw"),  # west along crosswalk to same intersection
        "south": (-1, 0, "ne"),  # south along avenue
    }
}


class Walker:
    def __init__(self,
                 walker_id: str,
                 street_idx: int,
                 avenue_idx: int,
                 corner: str,
                 speed: float,
                 destination_corner: tuple[int, int, str],
                 policy: str,
                 grid: CityGrid):
        self.id = walker_id
        self.street_idx = street_idx
        self.avenue_idx = avenue_idx
        self.corner = corner  # "nw", "ne", "sw", "se"
        self.speed = speed
        self.grid = grid
        self.policy = policy
        self.progress = 0.0
        self.destination_corner = destination_corner
        self.target = None
        self._set_next_target(world_time=0)

    def _set_next_target(self, world_time: float):
        nxt = None
        # Choose the next location based on the walker's policy
        # First, need to find directions required to reach destination

        n_s_axis = None
        e_w_axis = None

        # n_s_axis: +1 if walker should head north, -1 if should head south, 0 if on the correct j axis
        if self.destination_corner[0] != self.street_idx:
            n_s_axis = (self.destination_corner[0] - self.street_idx) / abs(self.destination_corner[0] - self.street_idx)
        elif self.destination_corner[2][0] == self.corner[0]:
            n_s_axis = 0
        elif self.destination_corner[2][0] == "n":
            n_s_axis = +1
        else:
            n_s_axis = -1

        # e_w_axis: +1 if walker should head east, -1 if should head west, 0 if on the correct i axis
        if self.destination_corner[1] != self.avenue_idx:
            e_w_axis = (self.destination_corner[1] - self.avenue_idx) / abs(self.destination_corner[1] - self.avenue_idx)
        elif self.destination_corner[2][1] == self.corner[1]:
            e_w_axis = 0
        elif self.destination_corner[2][1] == "e":
            e_w_axis = +1
        else:
            e_w_axis = -1

        # Observe the traffic light to see which direction
        intersection_traffic_light_offset = self.grid.traffic_light_grid[(self.avenue_idx, self.street_idx)]
        avenue_light_is_green = ((world_time + intersection_traffic_light_offset)
                                 % self.grid.traffic_light_cycle_length
                                 > self.grid.avenue_traffic_light_cycle_times[0])

        # If policy is 'avenue', then we will continue walking N/S until we hit the destination street or a red light, then turn
        if self.policy == "avenue":

            if n_s_axis == +1 and self.corner[0] == "n":
                nxt = _CORNER_DELTAS[self.corner]["north"]
            elif n_s_axis == -1 and self.corner[0] == "s":
                nxt = _CORNER_DELTAS[self.corner]["south"]
            elif avenue_light_is_green:
                if e_w_axis == +1:
                    nxt = _CORNER_DELTAS[self.corner]["east"]
                elif e_w_axis == -1:
                    nxt = _CORNER_DELTAS[self.corner]["west"]
                elif n_s_axis == +1:
                    nxt = _CORNER_DELTAS[self.corner]["north"]
                elif n_s_axis == -1:
                    nxt = _CORNER_DELTAS[self.corner]["south"]
                else:
                    nxt = None
            elif not avenue_light_is_green:
                if n_s_axis == +1:
                    nxt = _CORNER_DELTAS[self.corner]["north"]
                elif n_s_axis == -1:
                    nxt = _CORNER_DELTAS[self.corner]["south"]
                elif e_w_axis == +1:
                    nxt = _CORNER_DELTAS[self.corner]["east"]
                elif e_w_axis == -1:
                    nxt = _CORNER_DELTAS[self.corner]["west"]
                else:
                    nxt = None

        # If policy is 'street', then we will take the opportunity to cross the avenue along the street if it's green
        if self.policy == "street":

            if avenue_light_is_green:
                if e_w_axis == +1:
                    nxt = _CORNER_DELTAS[self.corner]["east"]
                elif e_w_axis == -1:
                    nxt = _CORNER_DELTAS[self.corner]["west"]
                elif n_s_axis == +1:
                    nxt = _CORNER_DELTAS[self.corner]["north"]
                elif n_s_axis == -1:
                    nxt = _CORNER_DELTAS[self.corner]["south"]
                else:
                    nxt = None
            elif not avenue_light_is_green:
                if n_s_axis == +1:
                    nxt = _CORNER_DELTAS[self.corner]["north"]
                elif n_s_axis == -1:
                    nxt = _CORNER_DELTAS[self.corner]["south"]
                elif e_w_axis == +1:
                    nxt = _CORNER_DELTAS[self.corner]["east"]
                elif e_w_axis == -1:
                    nxt = _CORNER_DELTAS[self.corner]["west"]
                else:
                    nxt = None

        # If policy is 'greedy', then we will take whatever light is available in the direction of our destination
        if self.policy == "greedy":
            intersection_traffic_light_offset = self.grid.traffic_light_grid[(self.avenue_idx, self.street_idx)]
            avenue_light_is_green = ((world_time + intersection_traffic_light_offset)
                                     % self.grid.traffic_light_cycle_length
                                     > self.grid.avenue_traffic_light_cycle_times[0])

            if avenue_light_is_green:
                if e_w_axis == +1:
                    nxt = _CORNER_DELTAS[self.corner]["east"]
                elif e_w_axis == -1:
                    nxt = _CORNER_DELTAS[self.corner]["west"]
                elif n_s_axis == +1:
                    nxt = _CORNER_DELTAS[self.corner]["north"]
                elif n_s_axis == -1:
                    nxt = _CORNER_DELTAS[self.corner]["south"]
                else:
                    nxt = None
            elif not avenue_light_is_green:
                if n_s_axis == +1:
                    nxt = _CORNER_DELTAS[self.corner]["north"]
                elif n_s_axis == -1:
                    nxt = _CORNER_DELTAS[self.corner]["south"]
                elif e_w_axis == +1:
                    nxt = _CORNER_DELTAS[self.corner]["east"]
                elif e_w_axis == -1:
                    nxt = _CORNER_DELTAS[self.corner]["west"]
                else:
                    nxt = None

        if nxt is None:
            # Stay in place if no neighbor
            self.target = (self.street_idx, self.avenue_idx, self.corner)
        else:
            dj, di, new_corner = nxt
            j = self.street_idx + dj
            i = self.avenue_idx + di
            self.target = (j, i, new_corner)
        self.progress = 0.0

    def update(self, dt: float, world_time: float):

        if self.target == (self.street_idx, self.avenue_idx, self.corner):
            # If the walker reached their corner, we're done, no updates to do
            return

        # Need to check if traffic light is green before crossing
        if (self.target[0] == self.street_idx
            and self.target[1] == self.avenue_idx
            and self.progress <= 0.0):

            # Get the avenue traffic light offset time
            intersection_traffic_light_offset = self.grid.traffic_light_grid[(self.avenue_idx, self.street_idx)]
            avenue_light_is_green = ((world_time + intersection_traffic_light_offset)
                                  % self.grid.traffic_light_cycle_length
                                  > self.grid.avenue_traffic_light_cycle_times[0])

            # Check which crosswalk we're using (represented as "ne", "se", "nw", "sw")
            if self.corner[0] != self.target[2][0]:
                # If the first letter is different, then it's a north/south crosswalk (ie. street crosswalk)
                if avenue_light_is_green:
                    # If avenue light is green, street light is red, skip update
                    # TODO: check policy to change target?
                    if self.policy == "greedy":
                        self._set_next_target(world_time=world_time)
                    return
            elif self.corner[1] != self.target[2][1]:
                # If the second letter is different, then it's a east/west crosswalk (ie. avenue crosswalk)
                if not avenue_light_is_green:
                    # If avenue light is not green, skip update
                    # TODO: check policy to change target?
                    if self.policy == "greedy":
                        self._set_next_target(world_time=world_time)
                    return
            else:
                raise Exception(f"Bad state, corner transition: {self.corner} -> {self.target[2]}")


        step = self.speed * dt / max(self.grid.street_spacing, self.grid.avenue_spacing)
        self.progress += step
        if self.progress >= 1.0:
            # Snap to target corner
            self.street_idx, self.avenue_idx, self.corner = self.target
            self._set_next_target(world_time=world_time)

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
            "start": (j0, i0, c0),
            "end": (j1, i1, c1),
            "destination": self.destination_corner
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
            w.update(dt, self.time)
        return SimulationState(
            time=self.time,
            walkers=[w.to_state() for w in self.walkers],
        )
