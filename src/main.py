import utils

from player import Player
from world import World

import pygame

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
    pygame.init()

    screen = utils.create_screen(SCREEN_SIZE)
    utils.set_fps_limit(FPS_LIMIT)
    utils.set_mouse_config()

    world = World(WORLD_MAP)
    player = Player(PLAYER_START)

    while True:
        events = pygame.event.get()
        utils.handle_events(events)

        screen.fill(pygame.Color("black"))

        world.render(screen)
        player.move()
        player.cast_ray()
        player.render(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
