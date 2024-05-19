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
        self._size = 3
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

    def cast_rays(self) -> None:
        view_start = self._current_angle - self._field_of_view / 2
        view_end = self._current_angle + self._field_of_view / 2
        view_step = math.pi / 18
        num_rays = int((view_end - view_start) / view_step)
        angles = [view_start + i * view_step for i in range(num_rays)]

        for angle in angles:
            self._cast_ray(angle)

    def _cast_ray(self, angle: float) -> None:
        screen_start = (self._x, self._y)
        world_start = self._to_world_coords(screen_start)
        snapped_start = self._snap_to_grid(world_start)
        dx, dy = math.cos(angle), math.sin(angle)

        world_x, world_y = world_start
        snapped_x, snapped_y = snapped_start

        step_x = 1 if dx > 0 else -1
        step_y = 1 if dy > 0 else -1

        intersections = []

        while True:
            next_grid_x = (
                world_x + step_x
                if int(world_x) == world_x
                else math.ceil(world_x) if dx > 0 else math.floor(world_x)
            )
            intersect_vx = world_x + (next_grid_x - world_x)
            intersect_vy = world_y + (intersect_vx - world_x) * (dy / dx)
            distance_v = self._distance((world_x, world_y), (intersect_vx, intersect_vy))

            next_grid_y = (
                world_y + step_y
                if int(world_y) == world_y
                else math.ceil(world_y) if dy > 0 else math.floor(world_y)
            )
            intersect_hy = world_y + (next_grid_y - world_y)
            intersect_hx = world_x + (intersect_hy - world_y) * (dx / dy)
            distance_h = self._distance((world_x, world_y), (intersect_hx, intersect_hy))

            if distance_v < distance_h:
                snapped_x += step_x
                world_x, world_y = intersect_vx, intersect_vy
                intersections.append((intersect_vx, intersect_vy))
            else:
                snapped_y += step_y
                world_x, world_y = intersect_hx, intersect_hy
                intersections.append((intersect_hx, intersect_hy))

            if self._world.is_wall(snapped_x, snapped_y):
                ray_start = screen_start
                last_intersection = intersections[-1]
                ray_end = self._to_screen_coords(last_intersection)

                pygame.draw.line(self._screen, self._colour, ray_start, ray_end)
                pygame.draw.circle(self._screen, Color("blue"), ray_end, self._size)

                for intersection in intersections[:-1]:
                    screen_intersection = self._to_screen_coords(intersection)
                    pygame.draw.circle(self._screen, Color("green"), screen_intersection, self._size)

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
    
    @staticmethod
    def _distance(start: tuple[float, float], end: tuple[float, float]) -> float:
        start_x, start_y = start
        end_x, end_y = end
        delta_x = end_x - start_x
        delta_y = end_y - start_y
        return math.sqrt(delta_x ** 2 + delta_y ** 2)
