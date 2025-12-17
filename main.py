import pygame
import sys

def main():
    pygame.init()

    # Constants
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("2D Pixel Pokémon-like Game")

    # Game loop
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # Clear screen with black

        # Draw (update game logic and render here)

        pygame.display.flip()
        clock.tick(60)  # Maintain 60 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()