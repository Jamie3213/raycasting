import pygame
from pygame import Color, Rect, Surface


class World:
    def __init__(self, world_map: list[list[int]]) -> None:
        self.world_map = world_map
        self.width = len(self.world_map[0])
        self.height = len(self.world_map)
        self._border = 1

    def render(self, screen: Surface) -> None:
        cell_size = self.get_cell_size(screen)
        world = self._parse(cell_size)
        for cell in world:
            pygame.draw.rect(screen, Color("white"), cell)

    def is_wall(self, x: int, y: int) -> bool:
        return self.world_map[y][x] == 1

    def _parse(self, cell_size: tuple[int, int]) -> list[Rect]:
        rects = []
        cell_width, cell_height = cell_size
        for y, row in enumerate(self.world_map):
            for x, cell in enumerate(row):
                if cell == 1:
                    rect = Rect(
                        (x * cell_width) - self._border,
                        (y * cell_height) - self._border,
                        cell_width - self._border,
                        cell_height - self._border,
                    )
                    rects.append(rect)

        return rects

    def get_cell_size(self, screen: Surface) -> tuple[int, int]:
        width, height = screen.get_size()
        cell_width = width // self.width
        cell_height = height // self.height
        return cell_width, cell_height
