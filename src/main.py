import math
import os

import pygame
from pygame import Color

import utils
from player import Player
from raycaster import Ray
from world import World

FPS_LIMIT = 60
SCREEN_SIZE = (800, 600)
PLAYER_START = (400, 320)
NUM_RAYS = 800


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
        # world.render(screen)

        player.move(world)
        # player.render(screen)

        # Perform raycasting
        num_rays = screen.get_width()
        view_start = player.angle - (player.field_of_view / 2)
        view_end = player.angle + (player.field_of_view / 2)
        view_step = (view_end - view_start) / num_rays
        angles = [view_start + i * view_step for i in range(num_rays)]

        for index, angle in enumerate(angles):
            ray_start = player.position
            ray = Ray(ray_start, angle)
            ray.cast(world)
            ray.render(screen, index, player.angle)

        pygame.display.flip()


if __name__ == "__main__":
    main()
