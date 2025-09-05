import pygame

from src.config import OutputMode
from src.model import CityGrid, Walker, CitySimulation, StreetCornerLocation
from src.view import Visualizer, Viewport

def run_simulation(cfg):
    # Initialize grid
    grid = CityGrid(
        num_streets=cfg.num_streets,
        num_avenues=cfg.num_avenues,
        street_block_length=cfg.street_block_length,
        street_crosswalk_length=cfg.street_crosswalk_length,
        avenue_block_length=cfg.avenue_block_length,
        avenue_crosswalk_length=cfg.avenue_crosswalk_length,
        avenue_traffic_light_cycle_times=cfg.avenue_traffic_light_cycle_times,
        traffic_light_grid_random_seed=cfg.traffic_light_grid_random_seed,
    )

    # Initialize walkers
    walkers = [
        Walker(
            walker_id=str(i),
            street_idx=0,
            avenue_idx=0,
            corner=cfg.walker_starting_corner,
            direction=cfg.walker_starting_direction,
            speed=cfg.walker_speed,
            grid=grid,
            target=(cfg.num_streets, cfg.num_avenues, "nw"),
        )
        for i in range(cfg.num_walkers)
    ]

    sim = CitySimulation(grid, walkers)

    if cfg.output_mode == OutputMode.JSON:
        for i in range(20):
            print(sim.step(1))

    elif cfg.output_mode == OutputMode.PYGAME:
        # Setup Pygame
        pygame.init()
        screen = pygame.display.set_mode((cfg.screen_width, cfg.screen_height))
        pygame.display.set_caption("City Simulation")
        viewport = Viewport(grid.width, grid.height, cfg.screen_width, cfg.screen_height)
        vis = Visualizer(screen, viewport)
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            dt = 1 / cfg.frame_rate
            state = sim.step(dt)
            vis.draw(state, grid)
            pygame.display.flip()
            clock.tick(cfg.frame_rate)

        pygame.quit()
