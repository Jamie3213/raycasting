import pygame
from pygame import Color, Rect, Surface

CellWidth = int
CellHeight = int
World = list[list[int]]


def render_world(
    world: World,
    cell_resolution: tuple[CellWidth, CellHeight],
    screen: Surface,
) -> None:
    cell_width, cell_height = cell_resolution
    rects = [
        Rect(x * cell_width, y * cell_height, cell_width, cell_height)
        for y, row in enumerate(world)
        for x, cell in enumerate(row)
        if cell == 1
    ]

    for rect in rects:
        pygame.draw.rect(screen, Color("white"), rect)
