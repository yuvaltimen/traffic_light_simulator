import pygame
from src.model import SimulationState, CityGrid


class Viewport:
    """Maps world coordinates to screen coordinates."""

    def __init__(self, world_width, world_height, screen_width, screen_height):
        self.world_width = world_width
        self.world_height = world_height
        self.screen_width = screen_width
        self.screen_height = screen_height

    def to_screen(self, x, y):
        screen_x = int(x / self.world_width * self.screen_width)
        screen_y = int(y / self.world_height * self.screen_height)
        return screen_x, screen_y


def draw_grid(screen, grid: CityGrid, viewport: Viewport, color=(0, 0, 0)):
    # Avenues (vertical lines)
    for left, right in grid.avenue_positions():
        lx, _ = viewport.to_screen(left, 0)
        rx, _ = viewport.to_screen(right, 0)
        pygame.draw.line(screen, color, (lx, 0), (lx, viewport.screen_height), 2)
        pygame.draw.line(screen, color, (rx, 0), (rx, viewport.screen_height), 2)

    # Streets (horizontal lines)
    for top, bottom in grid.street_positions():
        _, ty = viewport.to_screen(0, top)
        _, by = viewport.to_screen(0, bottom)
        pygame.draw.line(screen, color, (0, ty), (viewport.screen_width, ty), 2)
        pygame.draw.line(screen, color, (0, by), (viewport.screen_width, by), 2)


class Visualizer:
    """Responsible only for rendering states."""

    def __init__(self, screen, viewport: Viewport):
        self.screen = screen
        self.viewport = viewport

    def draw(self, state: SimulationState, grid: CityGrid):
        self.screen.fill((255, 255, 255))  # background

        draw_grid(self.screen, grid, self.viewport)

        # draw walkers
        for w in state.walkers:
            px, py = self.viewport.to_screen(w.x, w.y)
            pygame.draw.circle(self.screen, (255, 0, 0), (px, py), 8)
