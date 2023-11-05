import pygame
import sys
pygame.init()

width, height = 1280, 720
screen = pygame.display.set_mode((width, height))

# Colors
black = (0, 0, 0)

def fade_transition(screen, direction, speed=2):
    # Create a surface to cover the screen
    cover_surface = pygame.Surface((width, height))
    cover_surface.fill(black)

    if direction == "in":
        alpha = 255  # Fully opaque for fade-in
    else:
        alpha = 0  # Fully transparent for fade-out

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if direction == "in":
            alpha -= speed
            if alpha <= 0:
                alpha = 0
        else:
            alpha += speed
            if alpha >= 255:
                alpha = 255

        # Set the alpha value of the cover surface
        cover_surface.set_alpha(alpha)

        screen.fill(black)  # Fill the screen with the background color
        screen.blit(cover_surface, (0, 0))  # Blit the cover surface on top

        pygame.display.flip()
        clock.tick(60)

        if (direction == "in" and alpha == 0) or (direction == "out" and alpha == 255):
            running = False