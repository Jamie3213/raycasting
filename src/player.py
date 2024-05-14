import math

import pygame
from pygame import Color, Surface


class Player:
    def __init__(self, start: tuple[float, float]) -> None:
        self._x, self._y = start
        self._movement_speed = 0.1
        self._turn_speed = 0.01
        self._size = 5
        self._current_angle = 0

    def render(self, screen: Surface) -> None:
        current_position = self._get_position()
        current_direction = self._get_direction()
        pygame.draw.circle(screen, Color("red"), current_position, self._size)
        pygame.draw.line(screen, Color("red"), current_position, current_direction)

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

    # def _get_initial_direction(self) -> tuple[float, float]:
    #     # Start the player facing forwards.
    #     return self._x, self._y - self._view_distance

    def _get_position(self) -> tuple[float, float]:
        return self._x, self._y

    def _get_direction(self) -> tuple[float, float]:
        # As the player moves the mouse left and right, the direction
        # should rotate clockwise or anti-clockwise, respectively.
        delta_x, _ = pygame.mouse.get_rel()
        increment = delta_x * self._turn_speed

        self._current_angle = (self._current_angle + increment) % (2 * math.pi)
        dir_x = self._x + 75 * math.cos(self._current_angle)
        dir_y = self._y + 75 * math.sin(self._current_angle)

        return dir_x, dir_y