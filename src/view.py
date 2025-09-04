import pygame
from src.model import CityGrid, SimulationState

class Viewport:
    def __init__(self, world_width, world_height, screen_width, screen_height):
        self.world_width = world_width
        self.world_height = world_height
        self.screen_width = screen_width
        self.screen_height = screen_height

    def to_screen(self, x, y):
        sx = int((x / self.world_width) * self.screen_width)
        sy = int((y / self.world_height) * self.screen_height)
        return sx, sy

def draw_grid(screen, grid: CityGrid, viewport, color=(0, 0, 0)):
    font = pygame.font.SysFont("Arial", 16)

    # Avenues (vertical lines)
    for idx, (left, right) in enumerate(grid.avenue_positions()):
        lx, _ = viewport.to_screen(left, 0)
        rx, _ = viewport.to_screen(right, 0)
        pygame.draw.line(screen, color, (lx, 0), (lx, viewport.screen_height), 2)
        pygame.draw.line(screen, color, (rx, 0), (rx, viewport.screen_height), 2)

        pygame.draw.rect(screen, (0, 0, 255), (lx, 0, grid.avenue_crosswalk_length, viewport.screen_height))

        # Draw avenue label above the top
        label = font.render(f"Ave {idx+1}", True, color)
        label_rect = label.get_rect(center=( (lx+rx)//2, grid.avenue_crosswalk_length ))
        screen.blit(label, label_rect)

    # Streets (horizontal lines)
    for idx, (top, bottom) in enumerate(grid.street_positions()):
        _, ty = viewport.to_screen(0, top)
        _, by = viewport.to_screen(0, bottom)
        pygame.draw.line(screen, color, (0, ty), (viewport.screen_width, ty), 2)
        pygame.draw.line(screen, color, (0, by), (viewport.screen_width, by), 2)

        pygame.draw.rect(screen, (255, 255, 0), (0, ty, grid.street_crosswalk_length, viewport.screen_width))

        # Draw street label to the left
        label = font.render(f"St {idx+1}", True, color)
        label_rect = label.get_rect(center=(10, (ty+by)//2))
        screen.blit(label, label_rect)

class Visualizer:
    def __init__(self, screen, viewport):
        self.screen = screen
        self.viewport = viewport

    def draw(self, state: SimulationState, grid: CityGrid):
        self.screen.fill((255, 255, 255))

        # Draw streets/avenues normally
        draw_grid(self.screen, grid, self.viewport)

        # Highlight walker segments (corner-to-corner)
        for w in state.walkers:
            # Get segment start and end coordinates
            j0, i0, c0 = w["start"]
            j1, i1, c1 = w["end"]
            x0, y0 = grid.corner_xy(j0, i0, c0)
            x1, y1 = grid.corner_xy(j1, i1, c1)
            sx0, sy0 = self.viewport.to_screen(x0, y0)
            sx1, sy1 = self.viewport.to_screen(x1, y1)

            # Draw segment in red
            pygame.draw.line(self.screen, (255, 0, 0), (sx0, sy0), (sx1, sy1), 4)

        # Draw walkers on top of segments
        for w in state.walkers:
            px, py = self.viewport.to_screen(w["x"], w["y"])
            pygame.draw.circle(self.screen, (255, 0, 0), (px, py), 8)
