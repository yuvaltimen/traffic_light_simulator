import math

import pygame
from src.model import CityGrid, SimulationState

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
VIOLET = (128, 128, 0)
GREY = (128, 128, 128)

Red = (220, 50, 47)
Blue = (38, 139, 210)
Green = (133, 153, 0)
Orange = (203, 75, 22)
Purple = (108, 113, 196)
Teal = (42, 161, 152)
Pink = (211, 54, 130)
Gold = (181, 137, 0)
Turquoise = (0, 170, 200)
Lime = (0, 200, 100)

WALKER_COLOR_LIST = [Red, Blue, Green, Orange, Purple, Teal, Pink, Gold, Turquoise, Lime]


def time_to_color(dt: float = None) -> tuple[int, int, int]:
    """
    Returns an RGB color oscillating smoothly between bright teal and dark blue
    over a 10-second cycle.

    Parameters:
        dt (float): time in seconds. If None, uses current time.

    Returns:
        (r, g, b) tuple with values in [0, 255].
    """
    # Normalize time to a value between 0 and 1 over a 10 second period
    phase = (dt % 10) / 10.0

    # Oscillate with sine wave: goes 0 -> 1 -> 0 over the cycle
    alpha = 0.5 * (1 - math.cos(2 * math.pi * phase))

    # Define colors
    teal = (0, 255, 200)
    dark_blue = (0, 0, 139)

    # Interpolate
    r = int((1 - alpha) * teal[0] + alpha * dark_blue[0])
    g = int((1 - alpha) * teal[1] + alpha * dark_blue[1])
    b = int((1 - alpha) * teal[2] + alpha * dark_blue[2])

    return r, g, b


class Viewport:
    def __init__(self, world_width, world_height, screen_width, screen_height):
        self.world_width = world_width
        self.world_height = world_height
        self.screen_width = screen_width
        self.screen_height = screen_height

    @property
    def scale_x(self):
        """pixels per meter in x direction"""
        return self.screen_width / self.world_width

    @property
    def scale_y(self):
        """pixels per meter in y direction"""
        return self.screen_height / self.world_height

    def to_screen_length_x(self, dx):
        """Convert world length (x axis) → screen pixels"""
        return int(dx * self.scale_x)

    def to_screen_length_y(self, dy):
        """Convert world length (y axis) → screen pixels"""
        return int(dy * self.scale_y)

    def to_screen(self, x, y):
        sx = int((x / self.world_width) * self.screen_width)
        sy = int((y / self.world_height) * self.screen_height)
        return sx, sy

def draw_grid(scrn, grid: CityGrid, viewport, color=BLACK):

    # Avenues (vertical lines)
    for idx, (left, right) in enumerate(grid.avenue_positions()):
        lx, _ = viewport.to_screen(left, 0)
        rx, _ = viewport.to_screen(right, 0)

        pygame.draw.rect(
            scrn,
            GREY,
            (lx, 0, viewport.to_screen_length_x(grid.avenue_crosswalk_length) + 1, viewport.screen_height)
        )

        pygame.draw.line(scrn, color, (lx, 0), (lx, viewport.screen_height), 2)
        pygame.draw.line(scrn, color, (rx, 0), (rx, viewport.screen_height), 2)



    # Streets (horizontal lines)
    for idx, (top, bottom) in enumerate(grid.street_positions()):
        _, ty = viewport.to_screen(0, top)
        _, by = viewport.to_screen(0, bottom)

        pygame.draw.rect(
            scrn,
            GREY,
            (0, ty, viewport.screen_width, viewport.to_screen_length_y(grid.street_crosswalk_length) + 1)
        )

        pygame.draw.line(scrn, color, (0, ty), (viewport.screen_width, ty), 2)
        pygame.draw.line(scrn, color, (0, by), (viewport.screen_width, by), 2)





class Visualizer:
    def __init__(self, scrn, viewport):
        self.screen = scrn
        self.viewport = viewport

    def draw(self, state: SimulationState, grid: CityGrid):
        self.screen.fill(WHITE)

        traffic_light_length = 12
        traffic_light_width = 6

        # Draw streets/avenues normally
        draw_grid(self.screen, grid, self.viewport)

        # Traffic light animations
        for intersection_tuple, offset_time in grid.traffic_light_grid.items():
            avenue_light_color = GREEN if (state.time + offset_time) % grid.traffic_light_cycle_length > grid.avenue_traffic_light_cycle_times[0] else RED
            street_light_color = RED if avenue_light_color == GREEN else GREEN
            intersection_x, intersection_y = grid.intersection_xy(*intersection_tuple)
            tx, ty = self.viewport.to_screen(intersection_x, intersection_y)
            pygame.draw.rect(self.screen, avenue_light_color, (tx - (traffic_light_length / 2), ty - (traffic_light_width / 2), traffic_light_length, traffic_light_width))
            pygame.draw.rect(self.screen, street_light_color, (tx - (traffic_light_width / 2), ty - (traffic_light_length / 2), traffic_light_width, traffic_light_length))

        # Highlight walker segments (corner-to-corner)
        for w in state.walkers:

            # Highlight the destination corner for each walker
            dj, di, dc = w["destination"]
            xd, yd = grid.corner_xy(dj, di, dc)
            sxd, syd = self.viewport.to_screen(xd, yd)
            pygame.draw.circle(self.screen, time_to_color(state.time), (sxd, syd), 6)

            # Get segment start and end coordinates
            j0, i0, c0 = w["start"]
            j1, i1, c1 = w["end"]
            x0, y0 = grid.corner_xy(j0, i0, c0)
            x1, y1 = grid.corner_xy(j1, i1, c1)
            sx0, sy0 = self.viewport.to_screen(x0, y0)
            sx1, sy1 = self.viewport.to_screen(x1, y1)

            walker_color = WALKER_COLOR_LIST[int(w["id"])]

            # Draw segment in red
            pygame.draw.line(self.screen, (255, 0, 0), (sx0, sy0), (sx1, sy1), 4)

            # Draw walkers on top of segments
            px, py = self.viewport.to_screen(w["x"], w["y"])
            pygame.draw.circle(self.screen, walker_color, (px, py), 8 - int(w["id"]))