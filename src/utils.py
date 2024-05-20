import math
import sys

import pygame
from pygame.event import Event
from pygame.surface import Surface


def set_mouse_config() -> None:
    # Hide cursor and confine mouse to window.
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)


def set_fps_limit(limit: int) -> None:
    pygame.time.Clock().tick(limit)


def create_screen(size: tuple[int, int]) -> Surface:
    return pygame.display.set_mode(size)


def handle_events(events: list[Event]) -> None:
    for event in events:
        match event.type:
            case pygame.QUIT:
                _quit()
            case pygame.KEYDOWN:
                _handle_key_press(event)


def get_mouse_position() -> tuple[int, int]:
    return pygame.mouse.get_pos()


def get_screen_size() -> tuple[int, int]:
    return pygame.display.get_window_size()


def _quit() -> None:
    pygame.quit()
    sys.exit()


def _handle_key_press(event: Event) -> None:
    match event.key:
        case pygame.K_ESCAPE:
            _quit()


def to_world_coords(
    screen_coords: tuple[float, float], grid_size: tuple[int, int]
) -> tuple[float, float]:
    pos_x, pos_y = screen_coords
    grid_width, grid_height = grid_size
    return pos_x / grid_width, pos_y / grid_height


def to_screen_coords(
    world_coords: tuple[float, float], grid_size: tuple[int, int]
) -> tuple[float, float]:
    world_x, world_y = world_coords
    grid_width, grid_height = grid_size
    return world_x * grid_width, world_y * grid_height


def snap_to_grid(world_coords: tuple[float, float]) -> tuple[int, int]:
    world_x, world_y = world_coords
    return math.floor(world_x), math.floor(world_y)


def distance(start: tuple[float, float], end: tuple[float, float]) -> float:
    start_x, start_y = start
    end_x, end_y = end
    delta_x = end_x - start_x
    delta_y = end_y - start_y
    return math.sqrt(delta_x**2 + delta_y**2)
