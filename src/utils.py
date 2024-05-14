import pygame


def get_mouse_position() -> tuple[int, int]:
    return pygame.mouse.get_pos()


# import math

# import pygame
# from pygame import Color, Rect, Surface

# class Ray:
#     def __init__(self, start: Point, angle: float) -> None:
#         self._start = start
#         self._angle = angle
#         self._slope = self._get_slope()

#     def _get_slope(self) -> float:
#         return math.tan(self.angle)


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