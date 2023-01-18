from typing import Any, Callable

import attr
import pygame

from utils import LEFT_MB, ignore_callback, singleton


__all__ = (
    'DiscreteSprite',
    'AnimatedSprite',
    'ButtonSprite',
    'CursorSprite',
)


Callback = Callable
Event = pygame.event.EventType
Image = pygame.surface.Surface
Mask = pygame.mask.Mask
Sound = pygame.mixer.Sound
Sprite = pygame.sprite.Sprite


class DiscreteSprite(Sprite):
    def __init__(self,
                 *args: Any,
                 sheet: Image,
                 num_cols: int = 1,
                 num_rows: int = 1,
                 xy: tuple[int, int] = (0, 0),
                 compute_masks: bool = False,
                 **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.frames: list[Image] = []
        self.masks: list[Mask] = []
        self._cut_sheet(sheet, num_cols, num_rows, compute_masks=compute_masks)

        self._show_frame(0)
        self.rect.move_ip(*xy)

    def _refresh_image(self) -> None:
        self.image = self.frames[self.frame_idx]
        if self.masks:
            self.mask = self.masks[self.frame_idx]

    def _show_frame(self, idx: int) -> None:
        self.frame_idx = idx
        self._refresh_image()

    def _switch_frame(self) -> None:
        self._show_frame((self.frame_idx + 1) % len(self.frames))

    def _cut_sheet(self, sheet: Image, num_cols: int, num_rows: int, compute_masks: bool) -> None:
        self.rect = pygame.Rect(
            0, 0, sheet.get_width() // num_cols, sheet.get_height() // num_rows,
        )
        for row in range(num_rows):
            for col in range(num_cols):
                location = (self.rect.w * col, self.rect.h * row)
                frame = sheet.subsurface(pygame.Rect(location, self.rect.size))
                self.frames.append(frame)
                if compute_masks:
                    self.masks.append(pygame.mask.from_surface(frame))

    def scale_sprite(self, size: tuple[int, int]) -> None:
        self.frames = [
            pygame.transform.scale(frame, size)
            for frame in self.frames
        ]
        self._refresh_image()


class AnimatedSprite(DiscreteSprite):
    def __init__(self, *args: Any, delay: float = 1, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.delay = delay
        self.elapsed = 0

    def step(self, delta_time: float) -> None:
        self.elapsed += delta_time
        while self.elapsed >= self.delay:
            self.elapsed -= self.delay
            self._switch_frame()


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
            return

        match event.type:
            case pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and self.handle_escape:
                    self.on_click()
            case pygame.MOUSEBUTTONUP:
                if event.button == LEFT_MB and self.rect.collidepoint(event.pos):
                    self.on_click()
            case pygame.MOUSEMOTION:
                collides = self.rect.collidepoint(pygame.mouse.get_pos())
                self._show_frame(int(collides))
            case _:
                pass


@singleton
@attr.s(slots=True, kw_only=True)
class CursorSprite(AnimatedSprite):
    sound: Sound = attr.ib(default=None, init=False)
    is_on: bool = attr.ib(default=False, init=False)

    def __attrs_post_init__(self):
        from core import ResourceManager

        manager = ResourceManager()
        # self.sound = manager.get_sound('click.wav')

    def step(self, delta_time: float) -> None:
        if self.is_on:
            self.elapsed += delta_time
            while self.elapsed >= self.delay:
                self.elapsed -= self.delay
                self._switch_frame()
                if not self.frame_idx:
                    self.is_on = False

    def update(self, event: Event | None = None) -> None:
        if event.type is None:
            return

        match event.type:
            case pygame.MOUSEMOTION:
                self.rect = self.image.get_rect(topleft=event.pos)
            case pygame.MOUSEBUTTONUP:
                if event.button == LEFT_MB:
                    # self.sound.stop()
                    # self.sound.play()
                    self.is_on = True
                    self.elapsed = 0
                    self._show_frame(0)
