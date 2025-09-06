import pygame

from src.config import OutputMode
from src.model import CityGrid, Walker, CitySimulation
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
            walker_id="1",
            street_idx=0,
            avenue_idx=0,
            corner=cfg.walker_starting_corner,
            speed=cfg.walker_speed,
            grid=grid,
            destination_corner=(cfg.num_streets - 1, cfg.num_avenues - 1, "nw"),
            policy="greedy",
        ),
        Walker(
            walker_id="2",
            street_idx=0,
            avenue_idx=0,
            corner=cfg.walker_starting_corner,
            speed=cfg.walker_speed,
            grid=grid,
            destination_corner=(cfg.num_streets - 1, cfg.num_avenues - 1, "nw"),
            policy="avenue",
        ),
        Walker(
            walker_id="3",
            street_idx=0,
            avenue_idx=0,
            corner=cfg.walker_starting_corner,
            speed=cfg.walker_speed,
            grid=grid,
            destination_corner=(cfg.num_streets - 1, cfg.num_avenues - 1, "nw"),
            policy="street",
        )
    ]

    sim = CitySimulation(grid, walkers)

    if cfg.output_mode == OutputMode.JSON:
        for i in range(20):
            print(sim.step(1).__dict__)

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

    elif cfg.output_mode == OutputMode.STATISTICS:

        walker_costs = {
            walker.policy: 0
            for walker in sim.walkers
        }

        while not all(walker.destination_corner == (walker.street_idx, walker.avenue_idx, walker.corner) for walker in sim.walkers):
            dt = 1 / cfg.frame_rate
            sim.step(dt)
            for walker in sim.walkers:
                if walker.destination_corner != (walker.street_idx, walker.avenue_idx, walker.corner):
                    walker_costs[walker.policy] += dt

        print(walker_costs)
