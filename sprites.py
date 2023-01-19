'''Module for custom sprite types and subclasses'''

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


Callback = Callable[..., Any]
Event = pygame.event.EventType
Image = pygame.surface.Surface
Mask = pygame.mask.Mask
Sound = pygame.mixer.Sound
Sprite = pygame.sprite.Sprite


@attr.s(slots=True, kw_only=True, init=False)
class DiscreteSprite(Sprite):
    '''Sprites with several frames which are to switched manually'''

    frame_idx: int = attr.ib(default=0, init=False)
    frames: list[Image] = attr.ib(factory=list, init=False)
    masks: list[Mask] = attr.ib(factory=list, init=False)

    def __init__(self,
                 *args: Any,
                 sheet: Image,
                 num_cols: int = 1,
                 num_rows: int = 1,
                 xy: tuple[int, int] = (0, 0),
                 compute_masks: bool = False,
                 **kwargs: Any):
        '''
        Initialization of DiscreteSprite instance

        :param sheet: a surface with table-organized frames
        :param num_cols: # of columns in a table
        :param num_rows: # of rows in a table
        :param xy: sprite top-left corner position
        :param compute_masks: whether to compute masks or not
        '''

        super().__init__(*args, **kwargs)

        self.frames: list[Image] = []
        self.masks: list[Mask] = []
        self._cut_sheet(sheet, num_cols, num_rows)
        if compute_masks:
            self.compute_masks()

        self._show_frame(0)
        self.rect.move_ip(*xy)  # type: ignore

    def _refresh_image(self) -> None:
        '''
        Helper method for refreshing current frame and mask (if available)
        '''

        self.image = self.frames[self.frame_idx]  # type: ignore
        if self.masks:
            self.mask = self.masks[self.frame_idx]  # type: ignore

    def _show_frame(self, idx: int) -> None:
        '''
        Helper method for switching to the frame by index

        :param idx: index of a frame (0-indexed)
        '''

        self.frame_idx = idx
        self._refresh_image()

    def _switch_frame(self) -> None:
        '''
        Helper method for switching to the next frame in a cycle
        '''

        self._show_frame((self.frame_idx + 1) % len(self.frames))

    def _cut_sheet(self, sheet: Image, num_cols: int, num_rows: int) -> None:
        '''
        Helper method for cutting the frames out of a table-organized source image

        :param sheet: a surface with table-organized frames
        :param num_cols: # of columns in a table
        :param num_rows: # of rows in a table
        '''

        self.rect = pygame.Rect(  # type: ignore
            0, 0, sheet.get_width() // num_cols, sheet.get_height() // num_rows,
        )
        for row in range(num_rows):
            for col in range(num_cols):
                location = (self.rect.w * col, self.rect.h * row)
                frame = sheet.subsurface(pygame.Rect(location, self.rect.size))
                self.frames.append(frame)

    def compute_masks(self) -> None:
        '''
        Computes and stores masks for all frames
        '''

        self.masks = [
            pygame.mask.from_surface(frame)
            for frame in self.frames
        ]

    def scale_sprite(self, size: tuple[int, int]) -> None:
        '''
        Scales all frames to fit a fixed rectangle shape

        :param size: rectangle shape size
        '''

        self.frames = [
            pygame.transform.scale(frame, size)
            for frame in self.frames
        ]
        self._refresh_image()


@attr.s(slots=True, kw_only=True, init=False)
class AnimatedSprite(DiscreteSprite):
    '''Sprite with several frames switching automatically'''

    delay: float = attr.ib(default=1)

    elapsed: float = attr.ib(default=0, init=False)

    def __init__(self, *args: Any, delay: float = 1, **kwargs: Any) -> None:
        '''
        Initialization of AnimatedSprite instance

        :param delay: time between to sequential frames to show, in seconds
        '''

        super().__init__(*args, **kwargs)

        self.delay = delay

    def step(self, delta_time: float) -> None:
        '''
        Update internal state after some time elapsed

        :param delta_time: time elapsed, in seconds
        '''

        self.elapsed += delta_time
        while self.elapsed >= self.delay:
            self.elapsed -= self.delay
            self._switch_frame()


@attr.s(slots=True, kw_only=True, init=False)
class ButtonSprite(DiscreteSprite):
    '''Sprite class for all clickable buttons'''

    handle_escape: bool = attr.ib(default=False)
    on_click: Callback = attr.ib(default=ignore_callback)

    def __init__(self, *,
                 sheet: Image,
                 xy: tuple[int, int] = (0, 0),
                 handle_escape: bool = False,
                 on_click: Callback = ignore_callback):
        '''
        Initialization of ButtonSprite instance

        :param sheet: a surface with table-organized frames
        :param xy: sprite top-left corner position
        :param handle_escape: whether to simulate being clicked on pressing escape key event or not
        :param on_click: callback on being clicked
        '''

        super().__init__(
            sheet=sheet,
            num_cols=2,
            num_rows=1,
            xy=xy,
        )
        self.rect = self.image.get_rect(topleft=xy)  # type: ignore

        self.handle_escape = handle_escape
        self.on_click = on_click

    def handle_event(self, event: Event | None = None) -> None:
        '''
        Event handler method

        :param event: an event to handle (optional)
        '''

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
    '''Singleton cursor sprite class'''

    sound: Sound = attr.ib(default=None, init=False)
    is_on: bool = attr.ib(default=False, init=False)

    def __attrs_post_init__(self) -> None:
        '''Post-initialization'''

        from core import ResourceManager

        manager = ResourceManager()
        # self.sound = manager.get_sound('click.wav')

    def step(self, delta_time: float) -> None:
        '''
        Update internal state after some time elapsed

        :param delta_time: time elapsed, in seconds
        '''

        if self.is_on:
            self.elapsed += delta_time
            while self.elapsed >= self.delay:
                self.elapsed -= self.delay
                self._switch_frame()
                if not self.frame_idx:
                    self.is_on = False

    def handle_event(self, event: Event | None = None) -> None:
        '''
        Event handler method

        :param event: an event to handle (optional)
        '''

        if event.type is None:
            return

        match event.type:
            case pygame.MOUSEMOTION:
                self.rect = self.image.get_rect(topleft=event.pos)  # type: ignore
            case pygame.MOUSEBUTTONUP:
                if event.button == LEFT_MB:
                    # self.sound.stop()
                    # self.sound.play()
                    self.is_on = True
                    self.elapsed = 0
                    self._show_frame(0)
