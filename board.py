import pygame

#Board Settings
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE/2 - 5)
BOARD_WIDTH = SQUARE_SIZE * COLUMN_COUNT
BOARD_HEIGHT = SQUARE_SIZE * (ROW_COUNT+1)
BOARD_SIZE = (BOARD_WIDTH, BOARD_HEIGHT)
SCREEN = pygame.display.set_mode(BOARD_SIZE)

#Colors
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (152, 251, 152)


#Fonts
LABEL_FONT = pygame.font.SysFont("monospace", 14)
BUTTON_FONT = pygame.font.SysFont("monospace", 28)
TITLE_FONT = pygame.font.SysFont("monospace", 58)
GAME_FONT = pygame.font.SysFont("monospace", 60)

