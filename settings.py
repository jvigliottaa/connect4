import pygame
import textinput
from board import SCREEN, BLACK, WHITE, GREEN, TITLE_FONT, BUTTON_FONT, LABEL_FONT

start_game = False


def display_settings():

    player_input_box = textinput.InputBox(195, 300, 100, 32)
    ai_input_box = textinput.InputBox(415, 300, 100, 32)

    pygame.display.update()

    # Display settings screen
    while not start_game:
        SCREEN.fill(WHITE)
        events = pygame.event.get()

        player_input_box.draw(SCREEN)
        ai_input_box.draw(SCREEN)

        player_label = LABEL_FONT.render("Players (1-2)", 1, BLACK)
        SCREEN.blit(player_label, (195, 275))

        ai_label = LABEL_FONT.render("Computer Level (1-4)", 1, BLACK)
        SCREEN.blit(ai_label, (395, 275))

        start_button = pygame.Rect(306, 400, 92, 32)
        pygame.draw.rect(SCREEN, GREEN, start_button)

        start_label = BUTTON_FONT.render("START", 1, BLACK)
        SCREEN.blit(start_label, (310, 400))

        title = TITLE_FONT.render("CONNECT 4", 1, BLACK)
        SCREEN.blit(title, (200, 100))

        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and start_button.collidepoint(event.pos):

                try:
                    player_input_num = int(player_input_box.text)
                    if player_input_num == 2:
                        return [player_input_num, 0]
                except ValueError:
                    print("NAN")

                try:
                    ai_input_num = int(ai_input_box.text)
                    player_input_num = int(player_input_box.text)
                    if player_input_num == 1 and 4 >= ai_input_num >= 1:
                        return [player_input_num, ai_input_num]
                except ValueError:
                    print("NAN")

            player_input_box.handle_event(event)
            ai_input_box.handle_event(event)

        pygame.display.update()
        pygame.time.Clock().tick(30)





