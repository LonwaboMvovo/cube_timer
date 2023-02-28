import pygame
import time
import scrambler
import times
import cube

from platform import system


def main():
    global time_text_colour, scramble, scramble_text, scramble_text_rect, time_text, time_text_rect, ao5s_text, ao5s_text_rect, ao12s_text, ao12s_text_rect, new_scramble_text, new_scramble_text_rect

    # Times list
    read_times_list = times.get_times_list()
    if len(read_times_list.keys()) == 0:
        ao5 = "-"
        ao12 = "-"
    else:
        ao5 = read_times_list[str(len(read_times_list.keys()) - 1)]["ao5"]
        ao12 = read_times_list[str(len(read_times_list.keys()) - 1)]["ao12"]

    solving = False
    solve_time = 0

    quitting = True

    while True:
        # Clean screen
        screen.fill(screen_bg_colour)

        # Check events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quitting = True
                    pygame.quit()
                    exit()

                if event.key == pygame.K_SPACE:
                    if not solving:
                        time_text_colour = (0,221,0)
                    else:
                        scramble = scrambler.get_scramble()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if solving:
                        solving = False
                        current_time = time.time()
                        solve_time = current_time - start_time

                        times.add_times_list(read_times_list, scramble, round(solve_time, 2))

                        read_times_list = times.get_times_list()
                        ao5 = read_times_list[str(len(read_times_list.keys()) - 1)]["ao5"]
                        ao12 = read_times_list[str(len(read_times_list.keys()) - 1)]["ao12"]
                    else:
                        time_text_colour = "grey"
                        solving = True
                        start_time = time.time()

            if event.type == pygame.MOUSEBUTTONDOWN and new_scramble_text_rect.collidepoint(pygame.mouse.get_pos()):
                scramble = scrambler.get_scramble()

        # Mouse hover effects
        if (new_scramble_text_rect.collidepoint(pygame.mouse.get_pos())):
            # set the cursor to the hand cursor
            pygame.mouse.set_cursor(pygame.cursors.tri_left)
        else:
            # set the cursor to the default arrow cursor
            pygame.mouse.set_cursor(pygame.cursors.arrow)

        if solving:
            current_time = time.time()
            solve_time = current_time - start_time


        scramble_text, scramble_text_rect = scrambler.update_scramble(AnonymousPro_font,screen_width, screen, scramble, new_scramble_text, new_scramble_text_rect)

        time_text, time_text_rect = times.update_time(solve_time, time_text_colour, digit_char, digital_7_font, screen_width, screen_height, screen)
        ao5s_text, ao5s_text_rect = times.update_timer_ao5(AnonymousPro_font_aos, aos_text_colour, screen_width, screen_height, screen, ao5)
        ao12s_text, ao12s_text_rect = times.update_timer_ao12(AnonymousPro_font_aos, aos_text_colour, screen_width, screen_height, screen, ao12)
        cube.draw_scramble(scramble, screen_width, screen_height, screen)

        if quitting:
            screen.fill("grey", (screen_width/2 - 300, screen_height/2 - 150, 600, 350))
            pygame.draw.rect(screen, "black", (screen_width/2 - 300, screen_height/2 - 150, 600, 350), width = 5)

            screen.blit(exit_text, exit_text_rect)

            screen.blit(exit_text_question, exit_text_rect_question)

            screen.fill((34,136,221), (screen_width/2 + 30, screen_height/2 + 110, 100, 60))
            screen.blit(exit_text_no, exit_text_no_rect)

            screen.fill((34,136,221), (screen_width/2 + 160, screen_height/2 + 110, 100, 60))
            screen.blit(exit_text_yes, exit_text_yes_rect)

        pygame.display.update()


if __name__ == "__main__":
    # inits bruv
    pygame.init()

    # Digit character is different for formatting on different systems
    digit_char = "-"
    if system() == 'Windows':
        digit_char = "#"

    # Set window icon
    icon_surface = pygame.Surface((32, 32))
    icon_surface.fill('yellow', (0, 0, 10, 10))
    icon_surface.fill('yellow', (11, 0, 10, 10))
    icon_surface.fill('yellow', (22, 0, 10, 10))
    icon_surface.fill('red', (0, 11, 10, 10))
    icon_surface.fill('yellow', (11, 11, 10, 10))
    icon_surface.fill('green', (22, 11, 10, 10))
    icon_surface.fill('blue', (0, 22, 10, 10))
    icon_surface.fill('yellow', (11, 22, 10, 10))
    icon_surface.fill('white', (22, 22, 10, 10))
    pygame.display.set_icon(icon_surface)

    # Set Window title
    pygame.display.set_caption("TwistTimer")

    # Set background
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    screen_bg_colour = (0,34,51)
    screen.fill(screen_bg_colour)

    # Time display
    digital_7_font = pygame.font.Font("Fonts/digital-7.ttf", 250)
    time_text_colour = "grey"

    # Scramble display
    AnonymousPro_font = pygame.font.Font("Fonts/AnonymousPro.ttf", 30)
    scramble = scrambler.get_scramble()

    # New scramble display
    AnonymousPro_font_new_scramble = pygame.font.Font("Fonts/AnonymousPro.ttf", 20)
    new_scramble_text = AnonymousPro_font_new_scramble.render("next", True, (34,136,221))
    new_scramble_text_rect = new_scramble_text.get_rect(topright = (screen_width - 160, 70))

    # ao5 and ao12 display
    AnonymousPro_font_aos = pygame.font.Font("Fonts/AnonymousPro.ttf", 60)
    aos_text_colour = (34,136,221)

    # Exit pygame display
    AnonymousPro_font_exit = pygame.font.Font("Fonts/AnonymousPro.ttf", 40)
    exit_text = AnonymousPro_font_exit.render("Exit TwistTimer", True, "black")
    exit_text_rect = exit_text.get_rect(midtop = (screen_width/2 - 90, screen_height/2 - 110))

    AnonymousPro_font_exit_question = pygame.font.Font("Fonts/AnonymousPro.ttf", 30)
    exit_text_question = AnonymousPro_font_exit_question.render("Do you want to exit TwistTimer", True, "black")
    exit_text_rect_question = exit_text_question.get_rect(midtop = (screen_width/2 - 15, screen_height/2))

    exit_text_no = AnonymousPro_font_exit_question.render("No", True, "white")
    exit_text_no_rect = exit_text_no.get_rect(center = (screen_width/2 + 80, screen_height/2 + 140))

    exit_text_yes = AnonymousPro_font_exit_question.render("Yes", True, "white")
    exit_text_yes_rect = exit_text_yes.get_rect(center = (screen_width/2 + 210, screen_height/2 + 140))

    main()
