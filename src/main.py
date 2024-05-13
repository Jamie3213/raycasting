from utils import Player, World

import pygame
import sys

FPS_LIMIT = 60
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

WORLD_MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]


def main() -> None:
    pygame.time.Clock().tick(FPS_LIMIT)
    screen = pygame.display.set_mode(SCREEN_SIZE)
    world = World(WORLD_MAP)
    player = Player(start=(320, 240))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(pygame.Color("black"))

        player.move()
        world.render(screen)
        player.render(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
