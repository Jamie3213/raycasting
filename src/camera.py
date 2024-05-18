import math

from world import World

import pygame
from pygame import Color, Surface


def sign(a: float) -> int:
    return 1 if a >= 0 else -1

class Camera:
    def __init__(
        self,
        start: tuple[float, float],
        world: World,
        screen: Surface,
    ) -> None:
        self._x, self._y = start
        self._world = world
        self._screen = screen
        self._movement_speed = 0.2
        self._turn_speed = 0.01
        self._current_angle = (-1) * math.pi / 2  # Start facing forwards.
        self._view_distance = 500
        self._field_of_view = math.pi / 3
        self._size = 5
        self._colour = Color("red")

    def render(self, screen: Surface) -> None:
        current_position = (self._x, self._y)
        pygame.draw.circle(screen, self._colour, current_position, self._size)

    def move(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self._y -= self._movement_speed
        if keys[pygame.K_s]:
            self._y += self._movement_speed
        if keys[pygame.K_a]:
            self._x -= self._movement_speed
        if keys[pygame.K_d]:
            self._x += self._movement_speed

    def turn(self) -> None:
        delta_x, _ = pygame.mouse.get_rel()
        increment = delta_x * self._turn_speed
        self._current_angle = (self._current_angle + increment) % (2 * math.pi)

    def cast_ray(self) -> None:
        screen_start = (self._x, self._y)
        start_x, start_y = self._to_world_coords(screen_start)

        angle = self._current_angle
        dx, dy = math.cos(angle), math.sin(angle)
        
        next_vx = math.ceil(start_x) if dx > 0 else math.floor(start_x)
        next_vy = start_y + (next_vx - start_x) * (dy / dx)

        next_hy = math.ceil(start_y) if dy > 0 else math.floor(start_y)
        next_hx = start_x + (next_hy - start_y) * (dx / dy)

        next_v = (next_vx, next_vy)
        next_y = (next_hx, next_hy)

        screen_v = self._to_screen_coords(next_v)
        screen_y = self._to_screen_coords(next_y)

        pygame.draw.line(self._screen, self._colour, screen_start, screen_v)
        pygame.draw.circle(self._screen, Color("blue"), screen_v, self._size)
        pygame.draw.circle(self._screen, Color("green"), screen_y, self._size)

    def _to_world_coords(self, screen_coords: tuple[float, float]) -> tuple[float, float]:
        cell_width, cell_height = self._world.get_cell_size(self._screen)
        pos_x, pos_y = screen_coords
        world_x = pos_x / cell_width
        world_y = pos_y / cell_height
        return world_x, world_y
    
    def _to_screen_coords(self, world_coords: tuple[float, float]) -> tuple[float, float]:
        cell_width, cell_height = self._world.get_cell_size(self._screen)
        world_x, world_y = world_coords
        screen_x = world_x * cell_width
        screen_y = world_y * cell_height
        return screen_x, screen_y
    
    @staticmethod
    def _snap_to_grid(world_coords: tuple[float, float]) -> tuple[int, int]:
        world_x, world_y = world_coords
        snapped_x = math.floor(world_x)
        snapped_y = math.floor(world_y)
        return snapped_x, snapped_y
