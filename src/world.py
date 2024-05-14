import pygame
from pygame import Color, Rect, Surface


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
