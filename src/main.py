from player import Player
from world import World

import pygame
import sys

FPS_LIMIT = 60
SCREEN_SIZE = (640, 480)
PLAYER_START = (320, 320)

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
    player = Player(PLAYER_START)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(pygame.Color("black"))

        world.render(screen)
        player.move()
        player.render(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
