from button import Button
from drawing import Drawing
from settings import *
from level_menu import level_menu_main

pygame.init()


def main_menu():

    flag_next_start = ''

    def get_button_motion():
        flag_play = button_play.motion()
        flag_settings = button_settings.motion()
        flag_skins = button_skins.motion()
        flag_quit = button_quit.motion()
        flag_about = button_about.motion()
        return {"Play": flag_play,
                "Settings": flag_settings,
                "Skins": flag_skins,
                "Quit": flag_quit,
                "About": flag_about}

    def get_button_drawn():
        drawer.drawing_main_menu(color_count)
        drawer.drawing_button(button_play)
        drawer.drawing_button(button_settings)
        drawer.drawing_button(button_skins)
        drawer.drawing_button(button_quit)
        drawer.drawing_button(button_about)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    drawer = Drawing(screen)
    pygame.display.set_caption("Pac-Man")
    clock = pygame.time.Clock()
    color_count = 1

    screen.fill(BLACK)

    button_play = Button((325, 260), 150, 50, "Play", 15)
    button_settings = Button((325, 339), 150, 50, "Settings", 15)
    button_skins = Button((325, 418), 150, 50, "Skins", 15)
    button_quit = Button((325, 530), 150, 50, "Quit", 15)
    button_about = Button((325, 646), 150, 50, "About", 15)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        color_count += 1
        color_count %= 255

        get_button_drawn()
        dict_flags = get_button_motion()

        if dict_flags["Play"]:
            flag_next_start = "Play"
            break
            # level choosing
        if dict_flags["Settings"]:
            pass
            # settings changing
        if dict_flags["Skins"]:
            pass
            # skins choosing
        if dict_flags["Quit"]:
            exit()
        if dict_flags["About"]:
            pass
            # reading about

        pygame.display.flip()
        clock.tick(FPS)

    if flag_next_start == "Play":
        level_menu_main()


main_menu()
