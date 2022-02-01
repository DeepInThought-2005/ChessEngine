from itertools import count
from numpy import flip, isin
from constants import *
from pieces import *
import random

class Board:
    def __init__(self) -> None:
        self.board = [[0] * 8 for _ in range(8)]
        self.turn = ""
        self.direction = WHITE
        self.enpassant = () # for noting
        self.en_p = ()
        # for 50 moves rule
        self.advance_counter = 0
        self.move_counter = 0
        self.load_FEN(START_POSITION)
        self.resize_pieces(DEF_WIDTH // 8, DEF_HEIGHT // 8)
        self.set_every_pos()
        self.redos = []
        self.undos = [START_POSITION]
        self.sound_switch = ON


    def get_best_move(self):
        self.sound_switch = OFF
        maxPlayer = False
        if self.turn == WHITE:
            maxPlayer = True
        self.counter = 0
        best_move, eval = self.minimax(self, 1, -999999, 999999, maxPlayer, self.counter)
        print(self.counter)
        self.sound_switch = ON
        return best_move, eval

    def get_every_move(self, bo):
        board = bo.board
        moves = []
        for i in range(8):
            for j in range(8):
                if board[j][i] != 0 and board[j][i].color == self.turn:
                    for m in self.move_filter((j, i), board[j][i].get_valid_moves(bo)):
                        moves.append([(j, i), m])
        return moves
    
    def evaluate(self, bo):
        eval = 0
        for i in range(8):
            for j in range(8):
                if bo[j][i] != 0:
                    eval += bo[j][i].value

        return eval
        

    def minimax(self, bo, depth, alpha, beta, maxPlayer, maxColor):
        self.counter += 1
        if depth == 0 or bo.is_game_over():
            return None, self.evaluate(bo.board)
        
        moves = self.get_every_move(bo)
        if len(moves) == 0:
            if self.check(WHITE):
                return -999999
            return 0
        best_move = random.choice(moves)
        if maxPlayer:
            maxEval = -999999
            for move in moves:
                fen = self.create_FEN()
                self.move(move[0], move[1])
                eval = self.minimax(bo, depth-1, alpha, beta, False, maxColor)[1]
                self.load_FEN(fen)
                if eval > maxEval:
                    maxEval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return best_move, maxEval
        
        else:
            minEval = 999999
            for move in moves:
                fen = self.create_FEN()
                self.move(move[0], move[1])
                eval = self.minimax(bo, depth-1, alpha, beta, True, maxColor)[1]
                self.load_FEN(fen)
                if eval < minEval:
                    minEval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return best_move, minEval


    def is_game_over(self):
        return False
    
    def change_turn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def set_enpassant(self, s):
        if isinstance(self.board[s[0]][s[1]], Pawn):
            if self.board[s[0]][s[1]].check_enpassant(self.enpassant):
                self.en_p = self.enpassant

    def get_danger_moves(self, turn):
        moves = []
        for i in range(8):
            for j in range(8):
                if self.board[j][i] != 0:
                    if self.board[j][i].color == turn:
                        if isinstance(self.board[j][i], Pawn) or isinstance(self.board[j][i], King):
                            for move in self.board[j][i].get_danger_moves(self):
                                moves.append(move)
                        else:
                            for move in self.board[j][i].get_valid_moves(self):
                                moves.append(move)
        return moves

                    

    def check(self, turn):
        # get oppenents danger moves
        danger = self.get_danger_moves(flip_turn(turn))
        c, r = self.get_king(turn)
        if (c, r) in danger:
            return True
        return False

    def move_filter(self, s, moves):
        tb = self.create_copy(self.board)
        result = []
        for i ,m in enumerate(moves):
            tb.change_pos(s, m)
            if not tb.check(self.turn) and self.get_king(WHITE) and self.get_king(BLACK):
                result.append(moves[i])
            tb.change_pos(m, s)
            tb = self.create_copy(self.board)
        return result


    def move(self, s, e, valid_moves=[]):
        self.en_p = ()
        # for enpassant
        self.set_enpassant(s)


        if self.turn == self.board[s[0]][s[1]].color:
            if self.sound_switch == ON:
                valid_moves = self.move_filter(s, self.board[s[0]][s[1]].get_valid_moves(self))
            else:
                valid_moves = [e]
            if e in valid_moves:
                # for fen
                if self.board[e[0]][e[1]] != 0:
                    self.advance_counter = 0
                else:
                    self.advance_counter += 1
                if len(self.undos) % 2 == 0:
                    self.move_counter += 1
                
                if self.sound_switch == ON:
                    if self.board[e[0]][e[1]] == 0:
                        MOVE.play()
                    else:
                        CAPTURE.play()

                if isinstance(self.board[s[0]][s[1]], Pawn):
                    if self.en_p:
                        if abs(e[1] - self.en_p[1]) == 1 and e[0] == self.en_p[0]:
                            self.board[self.en_p[0]][self.en_p[1]] = 0
                            if self.sound_switch == ON:
                                CAPTURE.play()
                    if self.board[s[0]][s[1]].first:
                        self.enpassant = e
                    else:
                        self.enpassant = ()
                    self.board[s[0]][s[1]].first = False
                    self.advance_counter = 0


                if isinstance(self.board[s[0]][s[1]], Rook):
                    c, r = self.get_king(self.turn)
                    if self.direction == WHITE:
                        if s[0] > 4:
                            self.board[c][r].kingside = False
                        else:
                            self.board[c][r].queenside = False
                    else:
                        if s[0] > 4:
                            self.board[c][r].queenside = False
                        else:
                            self.board[c][r].kingside = False

                if isinstance(self.board[s[0]][s[1]], King):
                    if self.direction == WHITE:
                        if self.board[s[0]][s[1]].kingside and e[0] - s[0] >= 2:
                            self.change_pos((7, s[1]), (5, s[1]))
                        elif self.board[s[0]][s[1]].queenside and s[0] - e[0] >= 2:
                            self.change_pos((0, s[1]), (3, s[1]))
                    else:
                        if self.board[s[0]][s[1]].kingside and s[0] - e[0]:
                            self.change_pos((0, s[1]), (2, s[1]))
                        elif self.board[s[0]][s[1]].queenside and e[0] - s[0]:
                            self.change_pos((6, s[1]), (4, s[1]))

                    self.board[s[0]][s[1]].kingside = False
                    self.board[s[0]][s[1]].queenside = False

                self.change_pos(s, e)
                return True

        return False

    def promote(self, s, e):
        # get window resolution
        resolution = tk.Tk()
        width = resolution.winfo_screenwidth()
        height = resolution.winfo_screenheight()
        resolution.destroy()
        # Create Tkinter window to choose the promotion
        root = tk.Tk()
        root.title("Promote")
        root.geometry('110x400+' + str(width // 2 - 55) + '+' + str(height // 2 - 200))
        root.resizable(width=False, height=False)
        def close_window():
            if not self.promoted:
                self.row = s[1]
                self.col = s[0]
            self.set_pos()
            root.destroy()
            return False

        root.protocol("WM_DELETE_WINDOW", close_window)
        Font = ("Arial", 15)
        Width = 6
        Height = 3
        def Queening():
            self.board[e[0]][e[1]] = Queen(e[0], e[1], self.turn)
            root.destroy()
        def Rooking():
            self.board[e[0]][e[1]] = Rook(e[0], e[1], self.turn)
            root.destroy()
        def Bishoping():
            self.board[e[0]][e[1]] = Bishop(e[0], e[1], self.turn)
            root.destroy()
        def Knighting():
            self.board[e[0]][e[1]] = Knight(e[0], e[1], self.turn)
            root.destroy()

        
        buttonQ = tk.Button(root, text="Queen", height=Height, width=Width, font=Font, command=Queening)
        buttonR = tk.Button(root, text="Rook", height=Height, width=Width, font=Font, command=Rooking)
        buttonB = tk.Button(root, text="Bishop", height=Height, width=Width, font=Font, command=Bishoping)
        buttonN = tk.Button(root, text="Knight", height=Height, width=Width, font=Font, command=Knighting)
        buttonQ.grid(column=0, row=1)
        buttonR.grid(column=0, row=2)
        buttonB.grid(column=0, row=3)
        buttonN.grid(column=0, row=4)
        root.mainloop()

    def undo(self):
        if len(self.undos) > 1:
            fen = self.undos.pop()
            self.redos.append(fen)
            self.load_FEN(self.undos[-1])
            self.change_turn()

    def redo(self):
        if self.redos:
            fen = self.redos.pop()
            self.undos.append(fen)
            self.load_FEN(fen)


    def change_pos(self, s, e):
        self.board[e[0]][e[1]] = self.board[s[0]][s[1]]
        self.board[e[0]][e[1]].col = e[0]
        self.board[e[0]][e[1]].row = e[1]
        self.board[s[0]][s[1]] = 0
    
    def create_copy(self, board):
        tb = Board()
        for i in range(8):
            for j in range(8):
                tb.board[j][i] = board[j][i]
        return tb

    def create_FEN(self):
        fen = ""
        bo = self.board
        temp = 0
        for i in range(8):
            for j in range(8):
                if bo[j][i] != 0:
                    if temp != 0:
                        fen += str(temp)
                    temp = 0
                    fen += bo[j][i].sign
                else:
                    temp += 1
            if temp != 0:
                fen += str(temp)
            if i != 7:
                fen += '/'
            temp = 0

        fen += ' ' + self.turn + ' '
        k = 0
        c, r = self.get_king(WHITE)
        if self.board[c][r].kingside:
            k += 1
            fen += 'K'
        if self.board[c][r].queenside:
            fen += 'Q'
            k += 1

        c, r = self.get_king(BLACK)
        if self.board[c][r].kingside:
            fen += 'k'
            k += 1
        if self.board[c][r].queenside:
            fen += 'q'
            k += 1
        
        if k == 0:
            fen += '-'
        

        if self.en_p:
            if self.turn == WHITE:
                fen += ' ' + chr(97 + self.en_p[0]) + str(8 - self.en_p[1] - 1)
            if self.turn == BLACK:
                fen += ' ' + chr(97 + self.en_p[0]) + str(8 - self.en_p[1] + 1)
        else:
            fen += " -"

        fen += ' ' + str(self.advance_counter) + ' ' + str(self.move_counter)
        

        return fen
                


    def load_FEN(self, fen):
        def get_between_space(pos):
            s = ""
            if fen[pos] == ' ':
                while fen[pos+1] != ' ':
                    s += fen[pos+1]
                    pos += 1
            return s

        # fen = fen.replace(' ', '')
        fen += ' '
        self.board = [[0] * 8 for _ in range(8)]
        i = -1
        j = 0
        for k, x in enumerate(fen):
            if x == 'Q':
                i += 1
                self.board[i][j] = Queen(i, j, WHITE)
            elif x == 'K':
                i += 1
                self.board[i][j] = King(i, j, WHITE)
            elif x == 'B':
                i += 1
                self.board[i][j] = Bishop(i, j, WHITE)
            elif x == 'N':
                i += 1
                self.board[i][j] = Knight(i, j, WHITE)
            elif x == 'R':
                i += 1
                self.board[i][j] = Rook(i, j, WHITE)
            elif x == 'P':
                i += 1
                self.board[i][j] = Pawn(i, j, WHITE, WHITE)
            elif x == 'q':
                i += 1
                self.board[i][j] = Queen(i, j, BLACK)
            elif x == 'k':
                i += 1
                self.board[i][j] = King(i, j, BLACK)
            elif x == 'b':
                i += 1
                self.board[i][j] = Bishop(i, j, BLACK)
            elif x == 'n':
                i += 1
                self.board[i][j] = Knight(i, j, BLACK)
            elif x == 'r':
                i += 1
                self.board[i][j] = Rook(i, j, BLACK)
            elif x == 'p':
                i += 1
                self.board[i][j] = Pawn(i, j, BLACK, BLACK)
            elif x == '/':
                j += 1
                i = -1
            else:
                i += int(x)

            if i == 7 and j == 7:
                if fen[k + 2] == 'b':
                    self.turn = BLACK
                else:
                    self.turn = WHITE
                
                #KQkq
                k += 3
                st = get_between_space(k)
                count = 1
                if st == "-":
                    count = 2
                else:
                    for s in st:
                        if s == "K":
                            count += 1
                            c, r = self.get_king(WHITE)
                            self.board[c][r].kingside = True
                        elif s == "Q":
                            count += 1
                            c, r = self.get_king(WHITE)
                            self.board[c][r].queenside = True
                        elif s == "k":
                            count += 1
                            c, r = self.get_king(BLACK)
                            self.board[c][r].kingside = True
                        elif s == "q":
                            count += 1
                            c, r = self.get_king(BLACK)
                            self.board[c][r].queenside = True
                
                # enpassant
                k += count
                st = get_between_space(k)
                if st == '-':
                    count = 2
                else:
                    self.enpassant = (ord(st[0]) - 97, 8 - int(st[1]))
                    count = 3

                # 50 moves rule
                k += count
                st = get_between_space(k)
                self.advance_counter = int(st)

                k += 2
                st = get_between_space(k)
                self.move_counter = int(st)


                break

                    

    def get_king(self, color):
        for i in range(8):
            for j in range(8):
                if self.board[j][i] != 0:
                    if color == WHITE:
                        if self.board[j][i].sign == 'K':
                            return (j, i)
                    else:
                        if self.board[j][i].sign == 'k':
                            return (j, i)
        return ()

    def draw_pieces(self, win):
        for i in range(8):
            for j in range(8):
                if self.board[j][i] != 0:
                    self.board[j][i].draw(win)

    def resize_pieces(self, w, h):
        for i in range(8):
            for j in range(8):
                if self.board[j][i] != 0:
                    self.board[j][i].resize(w, h)

    def set_every_pos(self):
        for i in range(8):
            for j in range(8):
                if self.board[j][i] != 0:
                    self.board[j][i].set_pos()

    def print_board(self):
        for i in range(8):
            for j in range(8):
                if self.board[j][i] != 0:
                    font_color = ''
                    if self.board[j][i].color == WHITE:
                        font_color = '37m'
                    else:
                        font_color = '31m'
                    print("\033[1;" + font_color + self.board[j][i].sign + "\033[0m", end=' ')
                else:
                    print('.', end=' ')
            print()
        print()

    def print_bo(self, board):
        for i in range(8):
            for j in range(8):
                if board[j][i] != 0:
                    font_color = ''
                    if board[j][i].color == WHITE:
                        font_color = '37m'
                    else:
                        font_color = '31m'
                    print("\033[1;" + font_color + board[j][i].sign + "\033[0m", end=' ')
                else:
                    print('.', end=' ')
            print()
        print()