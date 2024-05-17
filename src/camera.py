import math

from world import World

import pygame
from pygame import Color, Surface


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

    def cast_ray(self, world: World, screen: Surface) -> None:
        screen_position = (self._x, self._y)
        world_position = self._to_world_coords(screen_position)
        snapped_position = self._snap_to_grid(world_position)

        # Work out how much we move in the x and y direction for
        # each unit step along a ray point in the direction of the
        # player's view.
        angle = self._current_angle
        dx, dy = math.cos(angle), math.sin(angle)
        
        # We can paratmetrise a ray start with start point (x0, y0)
        # on the world grid as (x0 + t_x * dx, y0 + t * dy) where t is
        # the distance along the ray. For the DDA line algorithm, we
        # essentially want to know how far we move along the ray when
        # we move one unit in the x or y direction. When dx is large,
        # we move further along the ray for each unit step in the x
        # direction compared to when dx is small. Moving one unit in
        # the x direction means moving from x to x + 1, i.e., we want
        # to know the valu of t such that t * dx = 1, which means that
        # t = 1 / abs(dx) (and the same applies to dy).
        step_x, step_y = 1 / abs(dx), 1 / abs(dy)
        world_x, world_y = world_position
        snapped_x, snapped_y = snapped_position
    
        dist_x = (
            (snapped_x + 1 - world_x) * step_x
            if dx > 0
            else (world_x - snapped_x) * step_x
        )
        dist_y = (
            (snapped_y + 1 - world_y) * step_y
            if dy > 0
            else (world_y - snapped_y) * step_y
        )

        while True:
            if dist_x < dist_y:
                snapped_x += 1 if dx > 0 else -1
                dist_x += step_x
            else:
                snapped_y += 1 if dy > 0 else -1
                dist_y += step_y

            if world.is_wall(snapped_x, snapped_y):
                ray_start = screen_position
                intersection = (dist_x, dist_y)
                ray_end = self._to_screen_coords(intersection)
                pygame.draw.line(screen, self._colour, ray_start, ray_end)
                pygame.draw.circle(screen, Color("blue"), ray_end, self._size)
                break
    
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