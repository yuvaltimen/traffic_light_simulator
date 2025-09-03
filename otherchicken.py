import pygame
import sys

# Initialize pygame
pygame.init()

# Screen setup
width, height = 600, 200
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dot Moving on a Line")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)

# Line setup
line_y = height // 2
dot_x = 50
dot_radius = 10
speed = 3  # must not be 0

clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update dot position
    dot_x += speed
    if dot_x >= width - dot_radius or dot_x <= dot_radius:
        speed = -speed  # Bounce back

    # Draw everything
    screen.fill(WHITE)
    pygame.draw.line(screen, BLACK, (0, line_y), (width, line_y), 2)
    pygame.draw.circle(screen, RED, (dot_x, line_y), dot_radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
