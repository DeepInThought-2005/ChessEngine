from calendar import c
from turtle import color
from constants import *
import tkinter as tk


class Piece:
    def __init__(self, col, row, color) -> None:
        self.col = col
        self.row = row
        self.x = 0
        self.y = 0
        self.color = color
        self.sign = ""
        self.img_type = None
        self.width = 0
        self.height = 0

    def resize(self, w, h):
        self.width = w
        self.height = h
        self.img = pygame.transform.scale(self.img_type, (w, h))
    

    def set_pos(self):
        self.x = self.width * self.col
        self.y = self.height * self.row

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def get_horizontal_moves(self, board):
        moves = []
        for i in range(self.col, 7):
            moves.append((i + 1, self.row))
            if board[i+1][self.row] == 0:
                pass
            elif board[i+1][self.row].color != self.color:
                break
            else:
                moves.pop()
                break

        for i in range(self.col, 0, -1):
            moves.append((i - 1, self.row))
            if board[i-1][self.row] == 0:
                pass
            elif board[i-1][self.row].color != self.color:
                break
            else:
                moves.pop()
                break
        return moves

    def get_vertical_moves(self, board):
        moves = []

        for j in range(self.row, 7):
            moves.append((self.col, j + 1))
            if board[self.col][j+1] == 0:
                pass
            elif board[self.col][j+1].color != self.color:
                break
            else:
                moves.pop()
                break
        for j in range(self.row, 0, -1):
            moves.append((self.col, j - 1))
            if board[self.col][j-1] == 0:
                pass
            elif board[self.col][j-1].color != self.color:
                break
            else:
                moves.pop()
                break
        return moves

    def get_diagonal_moves(self, board):
        moves = []
        # right down
        for i in range(1, min(8 - self.col, 8 - self.row)):
            moves.append((self.col+i, self.row+i))
            if board[self.col+i][self.row+i] == 0:
                pass
            elif board[self.col+i][self.row+i].color != self.color:
                break
            else:
                moves.pop()
                break

        # right up:
        for i in range(1, min(8 - self.col, self.row+1)):
            moves.append((self.col+i, self.row-i))
            if board[self.col+i][self.row-i] == 0:
                pass
            elif board[self.col+i][self.row-i].color != self.color:
                break
            else:
                moves.pop()
                break
        
        # left down
        for i in range(1, min(self.col+1, 8-self.row)):
            moves.append((self.col-i, self.row+i))
            if board[self.col-i][self.row+i] == 0:
                pass
            elif board[self.col-i][self.row+i].color != self.color:
                break
            else:
                moves.pop()
                break
        
        # left up
        for i in range(1, min(self.col+1, self.row+1)):
            moves.append((self.col-i, self.row-i))
            if board[self.col-i][self.row-i] == 0:
                pass
            elif board[self.col-i][self.row-i].color != self.color:
                break
            else:
                moves.pop()
                break

        return moves

    def check_bound(self, co):
        # return true if out of bound
        if co[0] < 0 or co[0] > 7 or co[1] < 0 or co[1] > 7:
            return True
        return False


    def draw_valid_moves(self, win, board):
        for m in board.move_filter((self.col, self.row), self.get_valid_moves(board)):
            if color_board[m[0]][m[1]] == WHITE:
                pygame.draw.rect(win, valid_move_color_w, (m[0] * self.width, m[1] * self.height, self.width, self.height))
            else:                    
                pygame.draw.rect(win, valid_move_color_b, (m[0] * self.width, m[1] * self.height, self.width, self.height))



class Rook(Piece):
    def __init__(self, col, row, color) -> None:
        super().__init__(col, row, color)
        if self.color == WHITE:
            self.value = 50
            self.sign = 'R'
            self.img_type = WR
        else:
            self.value = -50
            self.sign = 'r'
            self.img_type = BR

    def get_valid_moves(self, bo):
        board = bo.board
        moves = []
        for move in self.get_horizontal_moves(board):
            moves.append(move)
        for move in self.get_vertical_moves(board):
            moves.append(move)
        return moves
        

class Knight(Piece):
    def __init__(self, col, row, color) -> None:
        super().__init__(col, row, color)
        if self.color == WHITE:
            self.value = 30
            self.img_type = WN
            self.sign = 'N'
        else:
            self.value = -30
            self.img_type = BN
            self.sign = 'n'

    def get_valid_moves(self, bo):
        board = bo.board
        moves = []
        c = self.col
        r = self.row
        moves.append((c+1, r+2))
        moves.append((c+2, r+1))
        moves.append((c+2, r-1))
        moves.append((c+1, r-2))
        moves.append((c-1, r-2))
        moves.append((c-2, r-1))
        moves.append((c-2, r+1))
        moves.append((c-1, r+2))
        result = []
        for m in moves:
            if not self.check_bound(m):
                result.append(m)
        moves = []
        for re in result:
            moves.append(re)
            if board[re[0]][re[1]] != 0:
                if board[re[0]][re[1]].color == self.color:
                    moves.pop()
            
        
        del result

        return moves




class Bishop(Piece):
    def __init__(self, col, row, color) -> None:
        super().__init__(col, row, color)

        if self.color == WHITE:
            self.value = 30
            self.img_type = WB
            self.sign = 'B'
        else:
            self.value = -30
            self.img_type = BB
            self.sign = 'b'
    
    def get_valid_moves(self, bo):
        board = bo.board
        moves = []
        for move in self.get_diagonal_moves(board):
            moves.append(move)
        return moves
        

class Queen(Piece):
    def __init__(self, col, row, color) -> None:
        super().__init__(col, row, color)
        if self.color == WHITE:
            self.value = 90
            self.img_type = WQ
            self.sign = 'Q'
        else:
            self.value = -90
            self.sign = 'q'
            self.img_type = BQ

    def get_valid_moves(self, bo):
        board = bo.board
        moves = []
        for move in self.get_horizontal_moves(board):
            moves.append(move)
        for move in self.get_vertical_moves(board):
            moves.append(move)
        for move in self.get_diagonal_moves(board):
            moves.append(move)
        return moves

class King(Piece):
    def __init__(self, col, row, color) -> None:
        super().__init__(col, row, color)
        if self.color == WHITE:
            self.value = 10
            self.img_type = WK
            self.sign = 'K'
        else:
            self.value = -10
            self.sign = 'k'
            self.img_type = BK
        self.kingside = False
        self.queenside = False

    def get_danger_moves(self, bo):
        moves = self.get_valid_moves(bo)
        for i, m in enumerate(moves):
            if abs(m[0] - self.col) >= 2:
                del moves[i]
        return moves

    def get_valid_moves(self, bo):
        board = bo.board
        moves = []
        c, r = self.col, self.row
        moves.append((c+1, r-1))
        moves.append((c+1, r))
        moves.append((c+1, r+1))
        moves.append((c-1, r-1))
        moves.append((c-1, r))
        moves.append((c-1, r+1))
        moves.append((c, r-1))
        moves.append((c, r+1))

        result = []
        for m in moves:
            if not self.check_bound(m):
                result.append(m)
        moves = []
        for re in result:
            moves.append(re)
            if board[re[0]][re[1]] != 0:
                if board[re[0]][re[1]].color == self.color:
                    moves.pop()
        
        if bo.direction == WHITE:
            if self.color == WHITE:
                if self.kingside:
                    if board[5][7] == 0 and board[6][7] == 0:
                        moves.append((6, 7))
                if self.queenside:
                    if board[1][7] == 0 and board[2][7] == 0 and board[3][7] == 0:
                        moves.append((2, 7))
            else:
                if self.kingside:
                    if board[5][0] == 0 and board[6][0] == 0:
                        moves.append((6, 0))
                if self.queenside:
                    if board[1][0] == 0 and board[2][0] == 0 and board[3][0] == 0:
                        moves.append((2, 0))
        else:
            if self.color == BLACK:
                if self.kingside:
                    if board[1][7] == 0 and board[2][7] == 0:
                        moves.append((1, 7))
                if self.queenside:
                    if board[6][7] == 0 and board[5][7] == 0 and board[4][7] == 0:
                        moves.append((5, 7))
            else:
                if self.kingside:
                    if board[1][0] == 0 and board[2][0] == 0:
                        moves.append((1, 0))
                if self.queenside:
                    if board[6][0] == 0 and board[5][0] == 0 and board[4][0] == 0:
                        moves.append((5, 0))            

        return moves

class Pawn(Piece):
    def __init__(self, col, row, color, direction=WHITE) -> None:
        super().__init__(col, row, color)
        self.promoted = False
        self.direction = direction
        self.first = False
        if self.direction == WHITE:
            self.value = 10
            if self.row == 6:
                self.first = True
        else:
            self.value = -10
            if self.row == 1:
                self.first = True


        if self.color == WHITE:
            self.img_type = WP
            self.sign = 'P'
        else:
            self.sign = 'p'
            self.img_type = BP

    def get_danger_moves(self, bo):
        moves = []
        board = bo.board
        c, r = self.col, self.row
        if self.direction == WHITE:
             # for diagonal captures
            if c > 0 and r > 0 and board[c-1][r-1] != 0 and board[c-1][r-1].color != self.color:
                moves.append((self.col-1, self.row-1))
            if c < 7 and r > 0 and board[c+1][r-1] != 0 and board[c+1][r-1].color != self.color:
                moves.append((self.col+1, self.row-1))
        else:
            # for diagonal captures
            if c > 0 and r < 7 and board[c-1][r+1] != 0 and board[c-1][r+1].color != self.color:
                moves.append((self.col-1, self.row+1))
            if c < 7 and r < 7 and board[c+1][r+1] != 0 and board[c+1][r+1].color != self.color:
                moves.append((self.col+1, self.row+1))
        return moves


    def get_valid_moves(self, bo):
        board = bo.board
        moves = []
        c, r = self.col, self.row
        if self.direction == WHITE:
            if r  > 0 and board[c][r-1] == 0:
                moves.append((self.col, self.row-1))
            if self.first and board[c][r-2] == 0:
                moves.append((self.col, self.row-2))
            # for diagonal captures
            if c > 0 and r > 0 and board[c-1][r-1] != 0 and board[c-1][r-1].color != self.color:
                moves.append((self.col-1, self.row-1))
            if c < 7 and r > 0 and board[c+1][r-1] != 0 and board[c+1][r-1].color != self.color:
                moves.append((self.col+1, self.row-1))
        else:
            if r < 7 and board[c][r+1] == 0:
                moves.append((self.col, self.row+1))
            if self.first and board[c][r+2] == 0:
                moves.append((self.col, self.row+2))
            # for diagonal captures
            if c > 0 and r < 7 and board[c-1][r+1] != 0 and board[c-1][r+1].color != self.color:
                moves.append((self.col-1, self.row+1))
            if c < 7 and r < 7 and board[c+1][r+1] != 0 and board[c+1][r+1].color != self.color:
                moves.append((self.col+1, self.row+1))


        if bo.en_p:
            if abs(self.col - bo.en_p[0]) == 1 and self.row == bo.en_p[1] and bo.en_p[1] >= 3:
                if bo.direction == WHITE:
                    if self.color == WHITE:
                        moves.append((bo.en_p[0], bo.en_p[1]-1))
                    else:
                        moves.append((bo.en_p[0], bo.en_p[1]+1))
                else:
                    if self.color == WHITE:
                        moves.append((bo.en_p[0], bo.en_p[1]+1))
                    else:
                        moves.append((bo.en_p[0], bo.en_p[1]-1))

        return moves

    def check_enpassant(self, en_p):
        if en_p:
            if abs(self.col - en_p[0]) == 1 and self.row == en_p[1]:
                return True
        return False