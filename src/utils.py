import math

import pygame
from pygame import Color, Rect, Surface

CellWidth = int
CellHeight = int
Point = tuple[int, int]
World = list[list[int]]


def render_world(
    world: World,
    cell_resolution: tuple[CellWidth, CellHeight],
    screen: Surface,
) -> None:
    rects = _construct_world_rects(world, cell_resolution)
    for rect in rects:
        pygame.draw.rect(screen, Color("white"), rect)


def _construct_world_rects(world: World, cell_resolution: tuple[CellWidth, CellHeight]) -> list[Rect]:
    cell_width, cell_height = cell_resolution
    return [
        Rect(x * cell_width, y * cell_height, cell_width, cell_height)
        for y, row in enumerate(world)
        for x, cell in enumerate(row)
        if cell == 1
    ]


def cast_rays(start: Point, screen: Surface) -> None:
    number_of_rays = 360
    ray_length = 100
    angles = [math.radians(angle) for angle in range(number_of_rays)]

    for angle in angles:
        end = _construct_end_point(start, ray_length, angle)
        pygame.draw.circle(screen, Color("white"), start, 1)
        pygame.draw.line(screen, Color("white"), start, end)
        

def _construct_end_point(start: Point, length: int, angle: int) -> Point:
    x, y = start
    return (
        x + (length * math.cos(angle)),
        y + (length * math.sin(angle)),
    )
