import math

import pygame
from pygame import Color, Surface

from world import World


class Ray:
    def __init__(
        self,
        start: tuple[float, float],
        angle: float,
    ) -> None:
        self._x, self._y = start
        self._angle = angle
        self._intersections: list[tuple[float, float]] = []
        self._line_color = Color("black")
        self._intersect_color = Color("green")
        self._end_point_color = Color("blue")
        self._point_size = 3

    def cast(self, world: World) -> None:
        screen_start = (self._x, self._y)
        grid_size = world.get_grid_size()

        world_x, world_y = _to_world_coords(screen_start, grid_size)
        grid_x, grid_y = _snap_to_grid((world_x, world_y))
        dx, dy = (math.cos(self._angle), math.sin(self._angle))
        step_x, step_y = (1 if dx > 0 else -1, 1 if dy > 0 else -1)

        while True:
            # DDA algorithm - at each point, calculate the distance to the next
            # vertical and horizontal grid lines. If the vertical distance is
            # shorter, move one cell in the x-direction, otherwise move one cell
            # in the y-direction. Each time, check if the cell is a wall - if it
            # is, then stop, otherwise repeat the process from the intersection
            # point.
            next_grid_x = (
                world_x + step_x
                if int(world_x) == world_x
                else math.ceil(world_x) if dx > 0 else math.floor(world_x)
            )

            int_vx = world_x + (next_grid_x - world_x)
            int_vy = world_y + (int_vx - world_x) * (dy / dx)

            next_grid_y = (
                world_y + step_y
                if int(world_y) == world_y
                else math.ceil(world_y) if dy > 0 else math.floor(world_y)
            )

            int_hy = world_y + (next_grid_y - world_y)
            int_hx = world_x + (int_hy - world_y) * (dx / dy)

            dist_v = _distance((world_x, world_y), (int_vx, int_vy))
            dist_h = _distance((world_x, world_y), (int_hx, int_hy))

            if dist_v < dist_h:
                grid_x += step_x
                world_x, world_y = int_vx, int_vy
                intersect = _to_screen_coords((int_vx, int_vy), grid_size)
                self._intersections.append(intersect)
            else:
                grid_y += step_y
                world_x, world_y = int_hx, int_hy
                intersect = _to_screen_coords((int_hx, int_hy), grid_size)
                self._intersections.append(intersect)

            if world.is_wall(grid_x, grid_y):
                break

    def render(self, screen: Surface) -> None:
        ray_start = (self._x, self._y)
        ray_end = self._intersections[-1]

        # Render non-wall intersection points
        for point in self._intersections[:-1]:
            pygame.draw.circle(screen, self._intersect_color, point, self._point_size)

        # Render the ray and final wall intersection point
        pygame.draw.line(screen, self._line_color, ray_start, ray_end)
        pygame.draw.circle(screen, self._end_point_color, ray_end, self._point_size)


def _to_world_coords(
    screen_coords: tuple[float, float], grid_size: tuple[int, int]
) -> tuple[float, float]:
    pos_x, pos_y = screen_coords
    grid_width, grid_height = grid_size
    return pos_x / grid_width, pos_y / grid_height


def _to_screen_coords(
    world_coords: tuple[float, float], grid_size: tuple[int, int]
) -> tuple[float, float]:
    world_x, world_y = world_coords
    grid_width, grid_height = grid_size
    return world_x * grid_width, world_y * grid_height


def _snap_to_grid(world_coords: tuple[float, float]) -> tuple[int, int]:
    world_x, world_y = world_coords
    return math.floor(world_x), math.floor(world_y)


def _distance(start: tuple[float, float], end: tuple[float, float]) -> float:
    start_x, start_y = start
    end_x, end_y = end
    delta_x = end_x - start_x
    delta_y = end_y - start_y
    return math.sqrt(delta_x**2 + delta_y**2)
