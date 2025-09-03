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
        sx = int((x / self.world_width) * self.screen_width) if self.world_width > 0 else 0
        sy = int((y / self.world_height) * self.screen_height) if self.world_height > 0 else 0
        return sx, sy


def draw_grid(screen, grid: CityGrid, viewport: Viewport, color=(0, 0, 0)):
    """Draw centerlines only (where walkers move)."""
    # Avenues (vertical centerlines)
    for x in grid.avenue_centerlines():
        sx, _ = viewport.to_screen(x, 0)
        pygame.draw.line(screen, color, (sx, 0), (sx, viewport.screen_height), 2)

    # Streets (horizontal centerlines)
    for y in grid.street_centerlines():
        _, sy = viewport.to_screen(0, y)
        pygame.draw.line(screen, color, (0, sy), (viewport.screen_width, sy), 2)


class Visualizer:
    """Responsible only for rendering state snapshots."""

    def __init__(self, screen, viewport: Viewport):
        self.screen = screen
        self.viewport = viewport

    def draw(self, state: SimulationState, grid: CityGrid):
        self.screen.fill((255, 255, 255))
        draw_grid(self.screen, grid, self.viewport)

        # draw walkers from WalkerState (has x, y)
        for w in state.walkers:
            px, py = self.viewport.to_screen(w.x, w.y)
            pygame.draw.circle(self.screen, (255, 0, 0), (px, py), 8)
