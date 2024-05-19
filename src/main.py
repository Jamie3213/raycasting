import utils

from player import Player
from raycaster import Ray
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

    utils.set_fps_limit(FPS_LIMIT)
    utils.set_mouse_config()

    screen = utils.create_screen(SCREEN_SIZE)
    world = World(WORLD_MAP)
    player = Player(PLAYER_START)

    while True:
        events = pygame.event.get()
        utils.handle_events(events)

        world.render(screen)

        player.move()
        player.turn()
        player.render(screen)

        # Perform raycasting
        num_rays = 8
        view_start = player.angle - (player.field_of_view / 2)
        view_end = player.angle + (player.field_of_view / 2)
        view_step = (view_end - view_start) / num_rays
        angles = [view_start + i * view_step for i in range(num_rays)]

        for angle in angles:
            ray_start = player.x, player.y
            ray = Ray(ray_start, angle)
            ray.cast(world)
            ray.render(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
