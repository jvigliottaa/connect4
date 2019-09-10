import settings
import pygame
import numpy as np
import math
import sys
import random
import computer
from board import SCREEN, BLACK, RED, YELLOW, BLUE, SQUARE_SIZE, ROW_COUNT, COLUMN_COUNT, BOARD_WIDTH, RADIUS, \
    GAME_FONT, BOARD_HEIGHT


# Start settings screen and start game with correct settings
def start_settings():
    settings_info = settings.display_settings()

    pygame.init()
    board = create_board()
    draw_board(board)
    pygame.display.update()

    if settings_info[0] == 2:
        start_game_two_player(board)
    elif settings_info[0] == 1:
        start_game_one_player(board, settings_info[1])


# Start a two player game. Will allow for both players to make move
def start_game_two_player(board):
    game_over = False
    turn = 0

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(SCREEN, BLACK, (0, 0, BOARD_WIDTH, SQUARE_SIZE))
                pos_x = event.pos[0]
                if turn % 2 == 0:
                    pygame.draw.circle(SCREEN, RED, (pos_x, int(SQUARE_SIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(SCREEN, YELLOW, (pos_x, int(SQUARE_SIZE / 2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(SCREEN, BLACK, (0, 0, BOARD_WIDTH, SQUARE_SIZE))

                pos_x = event.pos[0]
                col = int(math.floor(pos_x / SQUARE_SIZE))

                # Click was a player one input
                if turn % 2 == 0:
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        # Check for win for player one
                        if check_for_win(board, 1):
                            game_over = True
                            label = GAME_FONT.render("PLAYER ONE WINS!!", 1, RED)
                            SCREEN.blit(label, (45, 10))

                # Click was a player two input
                else:
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        # Check for win for player two
                        if check_for_win(board, 2):
                            game_over = True
                            label = GAME_FONT.render("PLAYER TWO WINS!!", 1, YELLOW)
                            SCREEN.blit(label, (40, 10))

                draw_board(board)
                turn += 1

                # If game ended display winning title for 3 seconds before closing
                if game_over:
                    pygame.time.wait(3000)


# Start game for one player. Will create computer player
def start_game_one_player(board, difficulty):
    game_over = False
    computer_player = computer.ComputerPlayer(difficulty, board)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(SCREEN, BLACK, (0, 0, BOARD_WIDTH, SQUARE_SIZE))
                pos_x = event.pos[0]
                pygame.draw.circle(SCREEN, RED, (pos_x, int(SQUARE_SIZE / 2)), RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(SCREEN, BLACK, (0, 0, BOARD_WIDTH, SQUARE_SIZE))

                # Use click to get player one move
                pos_x = event.pos[0]
                col = int(math.floor(pos_x / SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if check_for_win(board, 1):
                        game_over = True
                        label = GAME_FONT.render("PLAYER ONE WINS!!", 1, RED)
                        SCREEN.blit(label, (45, 10))

                # Get move from AI
                col = computer_player.get_best_move()
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)
                if check_for_win(board, 2):
                    game_over = True
                    label = GAME_FONT.render("COMPUTER WINS!!", 1, YELLOW)
                    SCREEN.blit(label, (40, 10))

                draw_board(board)

                if game_over:
                    pygame.time.wait(3000)


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def check_for_win(board, tile):
    board_height = len(board[0])
    board_width = len(board)
    # check horizontal spaces
    for y in range(board_height):
        for x in range(board_width - 3):
            if board[x][y] != 0 and board[x][y] == tile and board[x + 1][y] == tile and board[x + 2][y] == tile and \
                    board[x + 3][y] == tile:
                return True

    # check vertical spaces
    for x in range(board_width):
        for y in range(board_height - 3):
            if board[x][y] == 0:
                continue
            if board[x][y] != 0 and board[x][y] == tile and board[x][y + 1] == tile and board[x][y + 2] == tile and \
                    board[x][y + 3] == tile:
                return True

    # check / diagonal spaces
    for x in range(board_width - 3):
        for y in range(3, board_height):
            if board[x][y] == 0:
                continue
            if board[x][y] != 0 and board[x][y] == tile and board[x + 1][y - 1] == tile and board[x + 2][
                    y - 2] == tile and board[x + 3][y - 3] == tile:
                return True

    # check \ diagonal spaces
    for x in range(board_width - 3):
        for y in range(board_height - 3):
            if board[x][y] == 0:
                continue
            if board[x][y] != 0 and board[x][y] == tile and board[x + 1][y + 1] == tile and board[x + 2][
                y + 2] == tile and board[x + 3][y + 3] == tile:
                return True
    return False


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(SCREEN, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(SCREEN, BLACK, (
                int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + (SQUARE_SIZE / 2))), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(SCREEN, RED, (
                    int(c * SQUARE_SIZE + SQUARE_SIZE / 2), BOARD_HEIGHT - int(r * SQUARE_SIZE + (SQUARE_SIZE / 2))),
                                   RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(SCREEN, YELLOW, (
                    int(c * SQUARE_SIZE + SQUARE_SIZE / 2), BOARD_HEIGHT - int(r * SQUARE_SIZE + (SQUARE_SIZE / 2))),
                                   RADIUS)
    pygame.display.update()


if __name__ == "__main__":
    start_settings()
