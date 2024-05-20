import os
import utils

from player import Player
from raycaster import Ray
from world import World

import pygame
from pygame import Color

FPS_LIMIT = 60
SCREEN_SIZE = (640, 480)
PLAYER_START = (320, 320)
NUM_RAYS = 8


def main() -> None:
    pygame.init()

    screen = utils.create_screen(SCREEN_SIZE)
    utils.set_fps_limit(FPS_LIMIT)
    utils.set_mouse_config()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    world_file = os.path.join(current_dir, "..", "data", "world.txt")
    world = World.from_file(world_file)
    player = Player(PLAYER_START)

    while True:
        events = pygame.event.get()
        utils.handle_events(events)

        screen.fill(Color("black"))
        world.render(screen)

        player.move()
        player.turn()
        player.render(screen)

        # Perform raycasting
        view_start = player.angle - (player.field_of_view / 2)
        view_end = player.angle + (player.field_of_view / 2)
        view_step = (view_end - view_start) / NUM_RAYS
        angles = [view_start + i * view_step for i in range(NUM_RAYS)]

        for angle in angles:
            ray_start = player.x, player.y
            ray = Ray(ray_start, angle)
            ray.cast(world)
            ray.render(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
