# import pygame
#
# # COLORS
#
# RED = (255, 0, 0)
# GREEN = (0, 255, 0)
# BLUE = (0, 0, 255)
# YELLOW = (255, 255, 0)
# PURPLE = (255, 0, 255)
# ORANGE = (255, 128, 0)
#
#
# class CityGrid:
#     def __init__(self, num_streets, num_avenues,
#                  street_block_length, street_crosswalk_length,
#                  avenue_block_length, avenue_crosswalk_length):
#         self.num_streets = num_streets
#         self.num_avenues = num_avenues
#         self.street_block_length = street_block_length
#         self.street_crosswalk_length = street_crosswalk_length
#         self.avenue_block_length = avenue_block_length
#         self.avenue_crosswalk_length = avenue_crosswalk_length
#
#         # total "world distance"
#         self.width = (num_avenues + 1) * avenue_block_length + num_avenues * avenue_crosswalk_length
#         self.height = (num_streets + 1) * street_block_length + num_streets * street_crosswalk_length
#
#     def avenue_positions(self):
#         """Return x coordinates (in world units) of all avenue lines."""
#         positions = []
#         for i in range(self.num_avenues):
#             left = avenue_x = self.avenue_block_length + i * (self.avenue_block_length + self.avenue_crosswalk_length)
#             right = left + self.avenue_crosswalk_length
#             positions.append((left, right))
#         return positions
#
#     def street_positions(self):
#         """Return y coordinates (in world units) of all street lines."""
#         positions = []
#         for i in range(self.num_streets):
#             top = self.street_block_length + i * (self.street_block_length + self.street_crosswalk_length)
#             bottom = top + self.street_crosswalk_length
#             positions.append((top, bottom))
#         return positions
#
#
# class Viewport:
#     def __init__(self, world_width, world_height, screen_width, screen_height):
#         self.world_width = world_width
#         self.world_height = world_height
#         self.screen_width = screen_width
#         self.screen_height = screen_height
#
#     def to_screen(self, x, y):
#         """Convert world coordinates (floats) to screen coordinates (ints)."""
#         screen_x = int(x / self.world_width * self.screen_width)
#         screen_y = int(y / self.world_height * self.screen_height)
#         return screen_x, screen_y
#
#
# def draw_grid(screen, grid, viewport, color=(0,0,0)):
#     # Avenues (vertical lines)
#     for left, right in grid.avenue_positions():
#         lx, _ = viewport.to_screen(left, 0)
#         rx, _ = viewport.to_screen(right, 0)
#         pygame.draw.line(screen, color, (lx, 0), (lx, viewport.screen_height), 2)
#         pygame.draw.line(screen, color, (rx, 0), (rx, viewport.screen_height), 2)
#
#     # Streets (horizontal lines)
#     for top, bottom in grid.street_positions():
#         _, ty = viewport.to_screen(0, top)
#         _, by = viewport.to_screen(0, bottom)
#         pygame.draw.line(screen, color, (0, ty), (viewport.screen_width, ty), 2)
#         pygame.draw.line(screen, color, (0, by), (viewport.screen_width, by), 2)
#
# class Walker:
#     def __init__(self, start_x, start_y, speed, grid: "CityGrid"):
#         self.x = start_x
#         self.y = start_y
#         self.speed = speed  # world units per second
#         self.grid = grid
#
#         # start by moving east (positive x)
#         self.dx, self.dy = 1, 0
#
#     def update(self, dt):
#         """Move walker forward by dt seconds, switching direction at intersections."""
#         self.x += self.dx * self.speed * dt
#         self.y += self.dy * self.speed * dt
#
#         # Check bounds and intersections
#         if self.dx != 0:  # moving along an avenue
#             if self.x >= self.grid.width or self.x <= 0:
#                 # clamp to edge
#                 self.x = max(0, min(self.x, self.grid.width))
#                 # turn south at corner
#                 self.dx, self.dy = 0, 1
#         elif self.dy != 0:  # moving along a street
#             if self.y >= self.grid.height or self.y <= 0:
#                 self.y = max(0, min(self.y, self.grid.height))
#                 # turn east again
#                 self.dx, self.dy = 1, 0
#
#
# def draw_walker(screen, walker, viewport, color=RED):
#     px, py = viewport.to_screen(walker.x, walker.y)
#     pygame.draw.circle(screen, color, (px, py), 8)
#
#
#
# def main():
#     pygame.init()
#     screen = pygame.display.set_mode((800, 800))
#     clock = pygame.time.Clock()
#
#     # Abstract city definition (world units, e.g. meters)
#     grid = CityGrid(
#         num_streets=6,
#         num_avenues=10,
#         street_block_length=20.0,
#         street_crosswalk_length=8.0,
#         avenue_block_length=30.0,
#         avenue_crosswalk_length=8.0
#     )
#
#     viewport = Viewport(grid.width, grid.height, 800, 800)
#
#     # Walker starting at top-left corner (0,0)
#     walker1 = Walker(start_x=0, start_y=0, speed=50.0, grid=grid)
#     walker2 = Walker(start_x=0, start_y=0, speed=40.0, grid=grid)
#
#     running = True
#     while running:
#         dt = clock.tick(60) / 1000.0  # seconds since last frame
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#
#         # Update walker
#         walker1.update(dt)
#         walker2.update(dt)
#
#         # Draw
#         screen.fill((255, 255, 255))
#         draw_grid(screen, grid, viewport)
#         draw_walker(screen, walker1, color=RED, viewport=viewport)
#         draw_walker(screen, walker2, color=BLUE, viewport=viewport)
#
#         pygame.display.flip()
#
#     pygame.quit()
#
#
# if __name__ == '__main__':
#     main()
