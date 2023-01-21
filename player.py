import pygame
from settings import *


class Player(pygame.sprite.Sprite):

    def __init__(self, group, pos):
        super().__init__(group)
        self.animation_tick = 0
        self.image = PLAYER_ANIMATION[self.animation_tick % 2]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.angle = 0
        self.key_pressed = 'a'
        self.moved = (-1, 0)
        self.score = 0

    def update(self):
        def is_next_wall(key_pressed):
            matrix_pos = (self.rect.y // 20, self.rect.x // 20)
            if key_pressed == 'a':
                if level_1_map[matrix_pos[0]][matrix_pos[1] - 1] not in ' O.':
                    if get_key(self.angle) == 'a' or get_key(self.angle) == 'd':
                        if self.rect.x % 20 == 0:
                            return True
                        else:
                            return False
                    elif get_key(self.angle) == 'w' or get_key(self.angle) == 's':
                        return True
                else:
                    if get_key(self.angle) == 'w' or get_key(self.angle) == 's':
                        if self.rect.y % 20 == 0:
                            return False
                        else:
                            return True
                    elif get_key(self.angle) == 'a' or get_key(self.angle) == 'd':
                        return False
            elif key_pressed == 's':
                if level_1_map[matrix_pos[0] + 1][matrix_pos[1]] not in ' O.':
                    if get_key(self.angle) == 's' or get_key(self.angle) == 'w':
                        if self.rect.y % 20 == 0:
                            return True
                        else:
                            return False
                    elif get_key(self.angle) == 'a' or get_key(self.angle) == 'd':
                        return True
                else:
                    if get_key(self.angle) == 'a' or get_key(self.angle) == 'd':
                        if self.rect.x % 20 == 0:
                            return False
                        else:
                            return True
                    elif get_key(self.angle) == 's' or get_key(self.angle) == 'w':
                        return False

            elif key_pressed == 'd':
                if level_1_map[matrix_pos[0]][matrix_pos[1] + 1] not in ' O.':
                    if get_key(self.angle) == 'a' or get_key(self.angle) == 'd':
                        if self.rect.x % 20 == 0:
                            return True
                        else:
                            return False
                    elif get_key(self.angle) == 'w' or get_key(self.angle) == 's':
                        return True
                else:
                    if get_key(self.angle) == 'w' or get_key(self.angle) == 's':
                        if self.rect.y % 20 == 0:
                            return False
                        else:
                            return True
                    elif get_key(self.angle) == 'a' or get_key(self.angle) == 'd':
                        return False

            elif key_pressed == 'w':
                if level_1_map[matrix_pos[0] - 1][matrix_pos[1]] not in ' O.':
                    if get_key(self.angle) == 's' or get_key(self.angle) == 'w':
                        if self.rect.y % 20 == 0:
                            return True
                        else:
                            return False
                    else:
                        return True
                else:
                    if get_key(self.angle) == 'a' or get_key(self.angle) == 'd':
                        if self.rect.x % 20 == 0:
                            return False
                        else:
                            return True
                    elif get_key(self.angle) == 's' or get_key(self.angle) == 'w':
                        return False

        def get_angle(key_pressed):
            if key_pressed == 'a':
                return 0
            elif key_pressed == 's':
                return 90
            elif key_pressed == 'd':
                return 180
            elif key_pressed == 'w':
                return 270

        def get_key(angle):
            if angle == 0:
                return 'a'
            elif angle == 90:
                return 's'
            elif angle == 180:
                return 'd'
            elif angle == 270:
                return 'w'

        def get_moved(key_pressed):
            if key_pressed == 'a':
                return -1, 0
            elif key_pressed == 's':
                return 0, 1
            elif key_pressed == 'd':
                return 1, 0
            elif key_pressed == 'w':
                return 0, -1

        self.rect.x %= 540
        self.rect.y %= 600

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.last_key_pressed = self.key_pressed
            self.key_pressed = 'a'
        if keys[pygame.K_s]:
            self.last_key_pressed = self.key_pressed
            self.key_pressed = 's'
        if keys[pygame.K_d]:
            self.last_key_pressed = self.key_pressed
            self.key_pressed = 'd'
        if keys[pygame.K_w]:
            self.last_key_pressed = self.key_pressed
            self.key_pressed = 'w'

        if not is_next_wall(self.key_pressed):
            self.moved = get_moved(self.key_pressed)
        else:
            if is_next_wall(get_key(self.angle)):
                self.moved = (0, 0)

        if self.moved == get_moved(self.key_pressed):
            self.angle = get_angle(self.key_pressed)

        self.rect = self.rect.move(self.moved)

        print(self.rect.x, self.rect.y)

        matrix_pos = (self.rect.y // 20, self.rect.x // 20)
        print(level_1_map[matrix_pos[0]][matrix_pos[1]])
        if level_1_map[matrix_pos[0]][matrix_pos[1]] == '.':
            print(self.rect.x // 20, self.rect.y // 20)
            level_1_map[matrix_pos[0]] = (level_1_map[matrix_pos[0]][:matrix_pos[1]] + ' ' +
                                          level_1_map[matrix_pos[0]][matrix_pos[1] + 1:])
            for point in points_sprites:
                if (point.rect.x // 20 == self.rect.x // 20 and point.rect.y // 20 == self.rect.y // 20 and
                        (self.angle == 90 or self.angle == 180)):
                    point.kill()
                    break
                if point.rect.x // 20 == ((self.rect.x + 20) // 20) and point.rect.y // 20 == self.rect.y // 20 \
                        and self.angle == 0:
                    point.kill()
                    break
                if point.rect.y // 20 == ((self.rect.y + 20) // 20) and point.rect.x // 20 == self.rect.x // 20 \
                        and self.angle == 270:
                    point.kill()
                    break
            self.score += 10
        elif level_1_map[matrix_pos[0]][matrix_pos[1]] == 'O':
            level_1_map[matrix_pos[0]] = (level_1_map[matrix_pos[0]][:matrix_pos[1]] + ' ' +
                                          level_1_map[matrix_pos[0]][matrix_pos[1] + 1:])
            self.score += 50

        self.animation_tick = (self.animation_tick + 2) % 25
        self.image = PLAYER_ANIMATION[self.animation_tick % 2]
        self.image = pygame.transform.rotate(self.image, self.angle)
