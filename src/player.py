import math

import pygame
from pygame import Color, Surface

import utils
from world import World


class Player:
    def __init__(self, start: tuple[float, float]) -> None:
        self.position = start
        self.angle = (-1) * math.pi / 2
        self.field_of_view = math.pi / 3

        self._movement_speed = self._get_movement_speed()
        self._turn_speed = 0.01
        self._size = 5
        self._color = Color("red")

    def _get_movement_speed(self) -> float:
        screen_width, screen_height = utils.get_screen_size()
        screen_area = screen_width * screen_height
        speed_multipler = screen_area / 100_000
        base_speed = 0.5
        return base_speed * speed_multipler

    def move(self, world: World) -> None:
        self._walk(world)
        self._turn()

    def _walk(self, world: World) -> None:
        dx, dy = 0.0, 0.0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            dx += math.cos(self.angle)
            dy += math.sin(self.angle)
        if keys[pygame.K_s]:
            dx -= math.cos(self.angle)
            dy -= math.sin(self.angle)
        if keys[pygame.K_a]:
            dx -= math.cos(self.angle + math.pi / 2)
            dy -= math.sin(self.angle + math.pi / 2)
        if keys[pygame.K_d]:
            dx += math.cos(self.angle + math.pi / 2)
            dy += math.sin(self.angle + math.pi / 2)

        if dx != 0 or dy != 0:
            length = math.hypot(dx, dy)
            norm_dx, norm_dy = dx / length, dy / length
            dx = norm_dx * self._movement_speed
            dy = norm_dy * self._movement_speed

            current_x, current_y = self.position
            next_position = (current_x + dx, current_y + dy)

            # Detect collisions with walls in the world grid.
            grid_size = world.get_grid_size()
            world_position = utils.to_world_coords(next_position, grid_size)
            snapped_x, snapped_y = utils.snap_to_grid(world_position)

            if not world.is_wall(snapped_x, snapped_y):
                self.position = next_position

    def _turn(self) -> None:
        delta_x, _ = pygame.mouse.get_rel()
        self.angle += delta_x * self._turn_speed

    def render(self, screen: Surface) -> None:
        pygame.draw.circle(screen, self._color, self.position, self._size)
