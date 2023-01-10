import pygame
from settings import *
from button import Button
from drawing import Drawing
from level_1 import level_1_main

pygame.init()


def back_to_menu():
    from main_menu import main_menu
    main_menu()


def level_menu_main():
    clock = pygame.time.Clock()

    def get_buttons_drawn():
        drawer.drawing_button(button_lev1)
        drawer.drawing_button(button_lev2)
        drawer.drawing_button(button_lev3)
        drawer.drawing_button(button_lev4)
        drawer.drawing_button(button_lev5)
        drawer.drawing_button(button_generate)
        drawer.drawing_button(button_back)

    def get_buttons_motion():
        flag_level1 = button_lev1.motion()
        flag_level2 = button_lev2.motion()
        flag_level3 = button_lev3.motion()
        flag_level4 = button_lev4.motion()
        flag_level5 = button_lev5.motion()
        flag_generate = button_generate.motion()
        flag_back = button_back.motion()
        return {"Level 1": flag_level1,
                "Level 2": flag_level2,
                "Level 3": flag_level3,
                "Level 4": flag_level4,
                "Level 5": flag_level5,
                "Generate level": flag_generate,
                "Back": flag_back
                }

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pac-Man")
    drawer = Drawing(screen)

    button_lev1 = Button((300, 193), 200, 40, "Level 1", 15)
    button_lev2 = Button((300, 253), 200, 40, "Level 2", 15)
    button_lev3 = Button((300, 313), 200, 40, "Level 3", 15)
    button_lev4 = Button((300, 373), 200, 40, "Level 4", 15)
    button_lev5 = Button((300, 433), 200, 40, "Level 5", 15)
    button_generate = Button((300, 533), 200, 40, "Generate level", 15)
    button_back = Button((300, 683), 200, 40, "Back", 15)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        drawer.drawing_level_menu()
        get_buttons_drawn()
        dict_flags = get_buttons_motion()

        pygame.display.flip()
        clock.tick(FPS)

        if dict_flags["Level 1"]:
            flag_next_start = "Level 1"
            break
        elif dict_flags["Level 2"]:
            pass
        elif dict_flags["Level 3"]:
            pass
        elif dict_flags["Level 4"]:
            pass
        elif dict_flags["Level 5"]:
            pass
        elif dict_flags["Generate level"]:
            pass
        elif dict_flags["Back"]:
            flag_next_start = "Back"
            break

    if flag_next_start == "Back":
        back_to_menu()
    elif flag_next_start == "Level 1":
        level_1_main()
