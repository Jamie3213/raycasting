import utils

import pygame
import sys

FPS_LIMIT = 60
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)


def main() -> None:
    pygame.time.Clock().tick(FPS_LIMIT)
    screen = pygame.display.set_mode(SCREEN_SIZE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(pygame.Color("black"))

        boundary = utils.Line((500, 50), (500, 350))
        utils.render_boundary(boundary, screen)

        mouse_position = pygame.mouse.get_pos()
        utils.cast_rays(mouse_position, boundary, screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
