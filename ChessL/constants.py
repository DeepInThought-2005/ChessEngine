import os
import pygame
pygame.mixer.init()

DEF_WIDTH = DEF_HEIGHT = 800

BLACK = 'b'
WHITE = 'w'
O_O = 'o-o'
O_O_O = 'o-o-o'

# GAME CONSTANTS
O_O = 'o-o'
O_O_O = 'o-o-o'
CHECKMATE = "checkmate"
STALEMATE = "stalemate"
DRAW = "draw"

# color
black = (0, 0, 0)
red = (255, 0, 0)
hell_red = (255, 60, 70)
valid_move_color_b = (186, 186, 0)
valid_move_color_w = (204, 204, 0)
capture_move_color = (204, 255, 255)
checked = (255, 128, 128)
select_color = (152, 152, 0)
panel_color = (160, 160, 160)

# sound
SOUNDTYPE = ".ogg"
CAPTURE = pygame.mixer.Sound(os.path.join("Sound", "capture" + SOUNDTYPE))
MOVE = pygame.mixer.Sound(os.path.join("Sound", "move" + SOUNDTYPE))
ON = "on"
OFF = "off"

# boardstyle
BLUE = 'blue'

BOARDSTYLE = BLUE
FILETYPE = '.png'

BOARD = pygame.image.load(os.path.join("Image/Boards", BOARDSTYLE + FILETYPE))
BOARD = pygame.transform.scale(BOARD, (DEF_WIDTH, DEF_HEIGHT))


# pieces

LICHESSDEFAULT = "LichessDefault"
STAUNTY = "Staunty"

PIECESTYLE = "Image/Pieces/" + STAUNTY

BK = pygame.image.load(os.path.join(PIECESTYLE, "bK" + FILETYPE))
BQ = pygame.image.load(os.path.join(PIECESTYLE, "bQ" + FILETYPE))
BR = pygame.image.load(os.path.join(PIECESTYLE, "bR" + FILETYPE))
BN = pygame.image.load(os.path.join(PIECESTYLE, "bN" + FILETYPE))
BB = pygame.image.load(os.path.join(PIECESTYLE, "bB" + FILETYPE))
BP = pygame.image.load(os.path.join(PIECESTYLE, "bP" + FILETYPE))

WK = pygame.image.load(os.path.join(PIECESTYLE, "wK" + FILETYPE))
WQ = pygame.image.load(os.path.join(PIECESTYLE, "wQ" + FILETYPE))
WR = pygame.image.load(os.path.join(PIECESTYLE, "wR" + FILETYPE))
WN = pygame.image.load(os.path.join(PIECESTYLE, "wN" + FILETYPE))
WB = pygame.image.load(os.path.join(PIECESTYLE, "wB" + FILETYPE))
WP = pygame.image.load(os.path.join(PIECESTYLE, "wP" + FILETYPE))

# game mode
HUMAN_AI = "human-ai"
HUMAN_HUMAN = "human-human"
AI_AI = "ai-ai"

START_POSITION = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


color_board = [[0] * 8 for _ in range(8)]
for i in range(8):
    for j in range(8):
        if j % 2 == 0:
            if i % 2 == 0:
                color_board[j][i] = WHITE
            else:
                color_board[j][i] = BLACK
        if j % 2 != 0:
            if i % 2 != 0:
                color_board[j][i] = WHITE
            else:
                color_board[j][i] = BLACK

def flip_turn(turn):
    if turn == WHITE:
        turn = BLACK
    else:
        turn = WHITE
    return turn