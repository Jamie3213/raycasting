import math

import pygame
from pygame import Color, Rect, Surface

Point = tuple[int, int]


class World:
    def __init__(self, world_map: list[list[int]]) -> None:
        self._world_map = world_map
        self._width = len(self._world_map[0])
        self._height = len(self._world_map)

    def render(self, screen: Surface) -> None:
        cell_size = self._get_cell_size(screen)
        world = self._parse(cell_size)
        for cell in world:
            pygame.draw.rect(screen, Color("white"), cell)

    def _parse(self, cell_size: tuple[int, int]) -> list[Rect]:
        rects = []
        border = 1
        cell_width, cell_height = cell_size
        for y, row in enumerate(self._world_map):
            for x, cell in enumerate(row):
                if cell == 1:
                    rect = Rect(
                        (x * cell_width) - border,
                        (y * cell_height) - border,
                        cell_width - border,
                        cell_height - border,
                    )
                    rects.append(rect)

        return rects

    def _get_cell_size(self, screen: Surface) -> tuple[int, int]:
        width, height = screen.get_size()
        cell_width = width // self._width
        cell_height = height // self._height
        return cell_width, cell_height
    

class Player:
    def __init__(self, start: Point) -> None:
        self._x, self._y = start
        self._speed = 0.1
        self._size = 5
        self._view_distance = 100
        self._current_direction = self._get_initial_direction()
        self._current_angle = 0
        self._previous_mouse_position = _get_mouse_position()
        pygame.mouse.set_pos([self._x, self._y])  # Set initial mouse position
        pygame.mouse.set_visible(False)  # Hide the mouse cursor
        pygame.event.set_grab(True)  # Confine the mouse cursor to the game window

    def render(self, screen: Surface) -> None:
        current_position = self._get_position()
        current_direction = self._get_direction()
        pygame.draw.circle(screen, Color("red"), current_position, self._size)
        pygame.draw.line(screen, Color("red"), current_position, current_direction)

    def move(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self._y -= self._speed
        if keys[pygame.K_s]:
            self._y += self._speed
        if keys[pygame.K_a]:
            self._x -= self._speed
        if keys[pygame.K_d]:
            self._x += self._speed

    def _get_initial_direction(self) -> tuple[float, float]:
        # Start the player facing forwards.
        return self._x, self._y - self._view_distance

    def _get_position(self) -> Point:
        return self._x, self._y

    def _get_direction(self) -> Point:
        # As the player moves the mouse left and right, the
        # direction should rotate clockwise or anti-clockwise,
        # respectively.
        cur_mouse_x, cur_mouse_y = _get_mouse_position()
        prev_mouse_x, _ = self._previous_mouse_position
        delta_x, _ = pygame.mouse.get_rel()  # Get the mouse movement delta
        increment = delta_x * 0.01

        self._current_angle = (self._current_angle + increment) % (2 * math.pi)

        dir_x = self._x + self._view_distance * math.cos(self._current_angle)
        dir_y = self._y + self._view_distance * math.sin(self._current_angle)

        self._previous_mouse_position = (cur_mouse_x, cur_mouse_y)
        return dir_x, dir_y

class Ray:
    def __init__(self, start: Point, angle: float) -> None:
        self._start = start
        self._angle = angle
        self._slope = self._get_slope()

    def _get_slope(self) -> float:
        return math.tan(self.angle)
    

def _get_mouse_position() -> Point:
    return pygame.mouse.get_pos()


# def _calculate_y_intercept(start: Point, slope: float | None) -> float:
#     x, y = start
#     return None if slope is None else y - (slope * x)


# def render_boundary(boundary: Line, screen: Surface) -> None:
#     pygame.draw.line(
#         screen, Color("white"), boundary.start, boundary.end
#     )


# def cast_rays(start: Point, boundary: Line, screen: Surface) -> None:
#     number_of_rays = 360
#     angles = [math.radians(angle) for angle in range(number_of_rays)]

#     for angle in angles:
#         ray = Ray(start, angle)
#         intersect = _calculate_intersect(ray, boundary)
#         if intersect is not None:
#             pygame.draw.circle(screen, Color("red"), start, 2)
#             pygame.draw.circle(screen, Color("red"), intersect, 2)
#             pygame.draw.line(screen, Color("white"), start, intersect)
        

# def _calculate_intersect(ray: Ray, boundary: Line) -> Point | None:
#     are_parallel = ray.slope == boundary.slope
#     if are_parallel:
#         return None
    
#     x_int = (
#         boundary.start[0]
#         if boundary.slope is None
#         else (boundary.y_intercept - ray.y_intercept) / (ray.slope - boundary.slope)
#     )
#     y_int = (ray.slope * x_int) + ray.y_intercept

#     intersect = (x_int, y_int)

#     if _is_on_line_segment(intersect, boundary):
#         return intersect

#     return None


# def _is_on_line_segment(point: Point, line: Line) -> bool:
#     x, y = point
#     x1, y1 = line.start
#     x2, y2 = line.end
#     return (x1 <= x <= x2 or x2 <= x <= x1) and (y1 <= y <= y2 or y2 <= y <= y1)