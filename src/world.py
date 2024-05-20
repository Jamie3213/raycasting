import utils
from typing import Self

import pygame
from pygame import Color, Rect, Surface


class World:
    def __init__(self, world_map: list[list[int]]) -> None:
        self.world_map = world_map
        self.width = len(self.world_map[0])
        self.height = len(self.world_map)
        self._wall_color = Color("grey")
        self._floor_color = Color("white")
        self._border = 1

    @classmethod
    def from_file(cls, path: str) -> Self:
        with open(path, mode="r") as file:
            serialized_world = file.readlines()

        rows = [
            [int(elem) for elem in row.split(",")]
            for row in serialized_world
        ]

        return cls(rows)

    def render(self, screen: Surface) -> None:
        grid_size = self.get_grid_size()
        world = self._parse(grid_size)
        for color, cell in world:
            pygame.draw.rect(screen, color, cell)

    def is_wall(self, x: int, y: int) -> bool:
        return self.world_map[y][x] == 1

    def _parse(self, grid_size: tuple[int, int]) -> tuple[Color, list[Rect]]:
        rects = []
        grid_width, grid_height = grid_size
        for y, row in enumerate(self.world_map):
            for x, cell in enumerate(row):
                color = self._wall_color if cell == 1 else self._floor_color
                rect = Rect(
                    (x * grid_width) - self._border,
                    (y * grid_height) - self._border,
                    grid_width - self._border,
                    grid_height - self._border,
                )
                rects.append((color, rect))

        return rects

    def get_grid_size(self) -> tuple[int, int]:
        screen_width, screen_height = utils.get_screen_size()
        grid_width = screen_width // self.width
        grid_height = screen_height // self.height
        return grid_width, grid_height
