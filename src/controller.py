import time
import pygame
import json
from src.model import CityGrid, Walker, CitySimulation
from src.view import Viewport, Visualizer
from src.config import Config, OutputMode


def run_simulation(cfg: Config):
    # --- Model setup ---
    grid = CityGrid(
        num_streets=cfg.num_streets,
        num_avenues=cfg.num_avenues,
        street_block_length=cfg.street_block_length,
        street_crosswalk_length=cfg.street_crosswalk_length,
        avenue_block_length=cfg.avenue_block_length,
        avenue_crosswalk_length=cfg.avenue_crosswalk_length,
    )

    walkers = [Walker(i, 0, 0, speed=cfg.walker_speed, grid=grid)
               for i in range(cfg.num_walkers)]
    sim = CitySimulation(grid, walkers)

    # --- Output mode ---
    if cfg.output_mode == OutputMode.PYGAME:
        pygame.init()
        screen = pygame.display.set_mode((cfg.screen_width, cfg.screen_height))
        clock = pygame.time.Clock()
        viewport = Viewport(grid.width, grid.height, cfg.screen_width, cfg.screen_height)
        vis = Visualizer(screen, viewport)

    running = True
    start_time = time.time()

    while running:
        dt = 1.0 / cfg.fps if cfg.output_mode != OutputMode.PYGAME else clock.tick(cfg.fps) / 1000.0

        # --- Exit conditions ---
        if cfg.max_time is not None and sim.time >= cfg.max_time:
            break
        if cfg.output_mode == OutputMode.PYGAME:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        # --- Step simulation ---
        state = sim.step(dt)

        # --- Handle outputs ---
        if cfg.output_mode == OutputMode.JSON:
            print(json.dumps({
                "time": state.time,
                "walkers": [
                    {"id": w.id, "x": w.x, "y": w.y, "dir": w.direction}
                    for w in state.walkers
                ]
            }))
        elif cfg.output_mode == OutputMode.PYGAME:
            vis.draw(state, grid)
            pygame.display.flip()
        elif cfg.output_mode == OutputMode.NONE:
            # Headless simulation only
            pass

    if cfg.output_mode == OutputMode.PYGAME:
        pygame.quit()
