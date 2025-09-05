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

        for intersection_tuple, offset_time in grid.traffic_light_grid.items():
            avenue_light_color = GREEN if (state.time + offset_time) % grid.traffic_light_cycle_length > grid.avenue_traffic_light_cycle_times[0] else RED
            street_light_color = RED if avenue_light_color == GREEN else GREEN
            intersection_x, intersection_y = grid.intersection_xy(*intersection_tuple)
            tx, ty = self.viewport.to_screen(intersection_x, intersection_y)
            pygame.draw.rect(self.screen, avenue_light_color, (tx - (traffic_light_length / 2), ty - (traffic_light_width / 2), traffic_light_length, traffic_light_width))
            pygame.draw.rect(self.screen, street_light_color, (tx - (traffic_light_width / 2), ty - (traffic_light_length / 2), traffic_light_width, traffic_light_length))

        # # Highlight walker segments (corner-to-corner)
        # for w in state.walkers:
        #     # Get segment start and end coordinates
        #     j0, i0, c0 = w["start"]
        #     j1, i1, c1 = w["end"]
        #     x0, y0 = grid.corner_xy(j0, i0, c0)
        #     x1, y1 = grid.corner_xy(j1, i1, c1)
        #     sx0, sy0 = self.viewport.to_screen(x0, y0)
        #     sx1, sy1 = self.viewport.to_screen(x1, y1)
        #
        #     # Draw segment in red
        #     pygame.draw.line(self.screen, (255, 0, 0), (sx0, sy0), (sx1, sy1), 4)
        #
        # # Draw walkers on top of segments
        # for w in state.walkers:
        #     px, py = self.viewport.to_screen(w["x"], w["y"])
        #     pygame.draw.circle(self.screen, (255, 0, 0), (px, py), 8)
