import pygame
import sys
from pygame import Color

import utils

FPS_LIMIT = 144

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

WORLD = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

CELL_WIDTH = SCREEN_WIDTH // len(WORLD[0])
CELL_HEIGHT = SCREEN_HEIGHT // len(WORLD)
CELL_RESOLUTION = (CELL_WIDTH, CELL_HEIGHT)


def main() -> None:
    pygame.time.Clock().tick(FPS_LIMIT)
    screen = pygame.display.set_mode(SCREEN_SIZE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(Color("black"))
        utils.render_world(WORLD, CELL_RESOLUTION, screen)

        mouse_position = pygame.mouse.get_pos()
        utils.cast_rays(mouse_position, screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
