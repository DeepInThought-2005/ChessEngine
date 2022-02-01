import pygame
from constants import *
from pieces import *
pygame.font.init()


class Control:
    def __init__(self, board) -> None:
        self.bo = board
        self.selected_pos = ()
        self.move_text = "Hi"
        self.mode = HUMAN_HUMAN


    def draw_window(self, win, w, h):
        board_img = pygame.transform.scale(BOARD, (w, h))
        win.blit(board_img, (0, 0))
        if self.bo.check(self.bo.turn):
            kp = self.bo.get_king(self.bo.turn)
            pygame.draw.rect(win, checked, (kp[0] * w // 8, kp[1] * h // 8, w // 8, h // 8))

        sp = self.selected_pos
        if self.selected_pos and self.bo.turn == self.bo.board[sp[0]][sp[1]].color:
            self.bo.board[sp[0]][sp[1]].draw_valid_moves(win, self.bo)
            # draw selected pos
            pygame.draw.rect(win, select_color, (sp[0] * w // 8, sp[1] * h // 8, w // 8, h // 8))
        self.bo.resize_pieces(w // 8, h // 8)
        self.bo.draw_pieces(win)
        #solve layer problem
        if self.selected_pos:
            self.bo.board[sp[0]][sp[1]].draw(win)

        # panel part
        pygame.draw.rect(win, panel_color, (w, 0, w // 4, h))
        font = pygame.font.SysFont('Times New Roman', 50)
        text = font.render(self.move_text, False, black)
        win.blit(text, (w + w // 8 - text.get_width() // 2, h // 2 - text.get_height() // 2))

        pygame.display.update()