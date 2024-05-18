import sys

import pygame
from pygame.event import Event
from pygame.surface import Surface


def set_mouse_config() -> None:
    # Hide cursor and confine mouse to window.
    pygame.mouse.set_visible(False)
    # pygame.event.set_grab(True)


def set_fps_limit(limit: int) -> None:
    pygame.time.Clock().tick(limit)


def create_screen(size: tuple[int, int]) -> Surface:
    return pygame.display.set_mode(size)


def handle_events(events: list[Event]) -> None:
    for event in events:
        match event.type:
            case pygame.QUIT: _quit()
            case pygame.KEYDOWN: _handle_key_press(event)


def get_mouse_position() -> tuple[int, int]:
    return pygame.mouse.get_pos()


def _quit() -> None:
    pygame.quit()
    sys.exit()


def _handle_key_press(event: Event) -> None:
    match event.key:
        case pygame.K_ESCAPE: _quit()
