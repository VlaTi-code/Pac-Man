from typing import Any, Callable

import attr
import pygame

from utils import ignore_callback, LEFT_MB


Callback = Callable
Event = pygame.event.EventType
Image = pygame.surface.Surface
Sprite = pygame.sprite.Sprite


class DiscreteSprite(Sprite):
    def __init__(self,
                 *args: Any,
                 sheet: Image,
                 num_cols: int = 1,
                 num_rows: int = 1,
                 xy: tuple[int, int] = (0, 0),
                 **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.frames: list[Image] = []
        self._cut_sheet(sheet, num_cols, num_rows)

        self._show_frame(0)
        self.rect.move_ip(*xy)

    def _show_frame(self, idx: int) -> None:
        self.frame_idx = idx
        self.image = self.frames[self.frame_idx]

    def _switch_frame(self) -> None:
        self._show_frame((self.frame_idx + 1) % len(self.frames))

    def _cut_sheet(self, sheet: Image, num_cols: int, num_rows: int) -> None:
        self.rect = pygame.Rect(
            0, 0, sheet.get_width() // num_cols, sheet.get_height() // num_rows,
        )
        for row in range(num_rows):
            for col in range(num_cols):
                location = (self.rect.w * col, self.rect.h * row)
                self.frames.append(sheet.subsurface(pygame.Rect(location, self.rect.size)))


class AnimatedSprite(DiscreteSprite):
    def __init__(self, *args: Any, delay: float = 1, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.delay = delay
        self.elapsed = 0

    def step(self, delta_time: float) -> None:
        self.elapsed += delta_time
        while self.elapsed >= self.delay:
            self.elapsed -= self.delay
            self._show_next()


class ButtonSprite(DiscreteSprite):
    def __init__(self, *,
                 sheet: Image,
                 xy: tuple[int, int] = (0, 0),
                 handle_escape: bool = False,
                 on_click: Callback = ignore_callback):
        super().__init__(
            sheet=sheet,
            num_cols=2,
            num_rows=1,
            xy=xy,
        )

        self.rect = self.image.get_rect(topleft=xy)

        self.handle_escape = handle_escape
        self.on_click = on_click

    def update(self, event: Event | None = None) -> None:
        if event is None:
            collides = self.rect.collidepoint(pygame.mouse.get_pos())
            self._show_frame(int(collides))
            return

        match event.type:
            case pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and self.handle_escape:
                    self.on_click()
            case pygame.MOUSEBUTTONUP:
                if event.button == LEFT_MB and self.rect.collidepoint(event.pos):
                    self.on_click()
            case _:
                pass


@attr.s(slots=True, kw_only=True)
class CursorSprite(DiscreteSprite):
    # probably a singleton
    # probably animated, not discrete
    pass


@attr.s(slots=True, kw_only=True)
class Particle(Sprite):
    # implement if necessary
    pass
