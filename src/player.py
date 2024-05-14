import math

import pygame
from pygame import Color, Surface


class Player:
    def __init__(self, start: tuple[float, float]) -> None:
        self._x, self._y = start
        self._movement_speed = 0.1
        self._turn_speed = 0.01
        self._current_angle = (-1) * math.pi / 2  # Start facing forwards.
        self._view_distance = 75
        self._field_of_view = math.pi / 3
        self._size = 5
        self._colour = Color("red")

    def render(self, screen: Surface) -> None:
        current_position = self._get_position()
        current_direction = self._get_direction()
        pygame.draw.circle(screen, self._colour, current_position, self._size)
        pygame.draw.line(screen, self._colour, current_position, current_direction)

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

    def cast_ray(self) -> None:
        ray_direction = self._get_direction()
        # print("Casting rays...")

    def _get_position(self) -> tuple[float, float]:
        return self._x, self._y

    def _get_direction(self) -> tuple[float, float]:
        # As the player moves the mouse left and right, the direction
        # should rotate clockwise or anti-clockwise, respectively.
        delta_x, _ = pygame.mouse.get_rel()
        increment = delta_x * self._turn_speed

        self._current_angle = (self._current_angle + increment) % (2 * math.pi)
        dir_x = self._x + self._view_distance * math.cos(self._current_angle)
        dir_y = self._y + self._view_distance * math.sin(self._current_angle)

        return dir_x, dir_y