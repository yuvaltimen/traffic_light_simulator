"""
The goal is to navigate a city grid system that optimizes time.
We will imagine an ideal city that has an infinite grid of
streets and avenues numbered 1,2,3...

We want to simulate the crossings given the following parameters:
- Start street
    (int): positive
- Start avenue
    (int): positive
- End street
    (int): positive
- End avenue
    (int): positive
- Street block length
    (float): distance measurement
- Avenue block length
    (float): distance measurement
- Walking speed
    (float): speed measurement
- Crossing times
    (?) not sure what this is...
- Light cycle length and green//red durations
    (tuple(float, float)): green, red times
"""
import sys
from math import floor

import pygame



def main():
    FRAME_RATE = 60
    WALKING_SPEED = 3.4
    STREET_BLOCK_LENGTH = 20.0
    STREET_CROSSWALK_LENGTH = 2.0
    AVENUE_BLOCK_LENGTH = 30.0
    AVENUE_CROSSWALK_LENGTH = 8.0

    LIGHT_CYCLE_RED_SECONDS, LIGHT_CYCLE_GREEN_SECONDS = 2.1, 1.1

    startStreet, startAvenue = 1, 2
    endStreet, endAvenue = 5, 4

    # Initialize pygame
    pygame.init()

    # Screen setup
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Dot Moving on a Line")

    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)




    prefer_cross_avenue = True


    # loop
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # make decision
        if prefer_cross_avenue:
            pass
        else:
            pass


        # draw the whole scene
        screen.fill(WHITE)

        num_avenues = 10
        num_streets = 6
        total_distance_x = ((num_avenues + 1) * AVENUE_BLOCK_LENGTH) + (num_avenues * AVENUE_CROSSWALK_LENGTH)
        total_distance_y = (num_streets + 1) * STREET_BLOCK_LENGTH  + (num_streets * STREET_CROSSWALK_LENGTH)

        pygame.draw.circle(screen, RED, (0, 0), 10)
        pygame.draw.circle(screen, RED, (0, screen_height), 10)
        pygame.draw.circle(screen, RED, (screen_width, 0), 10)
        pygame.draw.circle(screen, RED, (screen_width, screen_height), 10)

        for ave_block_num in range(num_avenues):
            percentage_1 = (AVENUE_BLOCK_LENGTH + (ave_block_num * (AVENUE_BLOCK_LENGTH + AVENUE_CROSSWALK_LENGTH))) / total_distance_x
            line_1_x = floor(percentage_1 * screen_width)
            percentage_2 = (AVENUE_BLOCK_LENGTH + AVENUE_CROSSWALK_LENGTH +  (ave_block_num * (AVENUE_BLOCK_LENGTH + AVENUE_CROSSWALK_LENGTH))) / total_distance_x
            line_2_x = floor(percentage_2 * screen_width)

            pygame.draw.line(screen, BLACK, (line_1_x, 0), (line_1_x, screen_height), 2)
            pygame.draw.line(screen, BLACK, (line_2_x, 0), (line_2_x, screen_height), 2)


        for street_block_num in range(num_streets):
            percentage_1 = (STREET_BLOCK_LENGTH + (street_block_num * (STREET_BLOCK_LENGTH + STREET_CROSSWALK_LENGTH))) / total_distance_y
            line_1_y = floor(percentage_1 * screen_height)
            percentage_2 = (STREET_BLOCK_LENGTH + STREET_CROSSWALK_LENGTH + (street_block_num * (STREET_BLOCK_LENGTH + STREET_CROSSWALK_LENGTH))) / total_distance_y
            line_2_y = floor(percentage_2 * screen_height)

            pygame.draw.line(screen, BLACK, (0, line_1_y), (screen_width, line_1_y), 2)
            pygame.draw.line(screen, BLACK, (0, line_2_y), (screen_width, line_2_y), 2)



        # Update dot position
        # dot_x += speed
        # if dot_x >= screen_width - dot_radius or dot_x <= dot_radius:
        #     speed = -speed  # Bounce back


        pygame.display.flip()
        clock = pygame.time.Clock()
        clock.tick(FRAME_RATE)

    pygame.quit()
    sys.exit()



if __name__ == '__main__':
    main()
