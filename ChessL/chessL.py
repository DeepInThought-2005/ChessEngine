import asyncio
import platform
import sys
import pygame
from constants import *
from board import *
from control import *

def get_square_onclick(m_x, m_y, w, h):
    for j in range(8):
        for i in range(8):
            if m_x >= i * w and m_x <= i * w + w and m_y >= j * h and m_y <= j * h + h:
                return i, j

def fit_browser_canvas():
    # pygbag sizes the page canvas before the game opens its window; resize it
    # again so the board and side panel keep their shape in the browser.
    if sys.platform == "emscripten":
        platform.window.window_resize()

async def main():
    def AI_move():
        fen = control.bo.create_FEN()
        move = control.bo.get_best_move()[0]
        control.bo.load_FEN(fen)
        control.bo.resize_pieces(w, h)
        control.bo.set_every_pos()
        if control.bo.move(move[0], move[1]):
            # for promotion
            s, e = move
            if isinstance(control.bo.board[e[0]][e[1]], Pawn):
                if e[1] == 0 or e[1] == 7:
                    # maybe a seperate function for the AI promotion
                    control.bo.board[e[0]][e[1]] = Queen(e[0], e[1], control.bo.turn)
                    control.bo.resize_pieces(w, h)
                    control.bo.set_every_pos()
            todo_after_move()
            c, r = move[0]
            x, y = move[1]
            control.move_text = chr(97 + c) + str(8-r) + '-' + chr(97 + x) + str(8-y)

    def todo_after_move():
        fen = control.bo.create_FEN()
        if control.bo.redos:
            if control.bo.redos[-1] != fen:
                control.bo.redos =  []                        
        control.bo.undos.append(fen)
        control.bo.print_board()
        print(control.bo.create_FEN())
        control.bo.change_turn()

    run = True
    # In the browser the page scales the canvas; a resizable window would be
    # stretched to the page's shape instead.
    flags = 0 if sys.platform == "emscripten" else pygame.RESIZABLE
    win = pygame.display.set_mode((DEF_WIDTH + DEF_WIDTH // 4, DEF_HEIGHT), flags)
    board = Board()
    control = Control(board)

    pygame.display.set_caption("ChessL")
    last_size = None
    fit_browser_canvas()
    while run:
        width = int(win.get_width() * 4 // 5)
        height = win.get_height()
        w = width // 8
        h = height // 8
        control.bo.w = w
        control.bo.h = h
        if (w, h) != last_size:
            # The window can change size (and does when the browser fits the canvas);
            # keep the pieces on their squares.
            last_size = (w, h)
            control.bo.resize_pieces(w, h)
            control.bo.set_every_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = event.pos
                if m_x < width:
                    x, y = get_square_onclick(m_x, m_y, w, h)
                    if event.button == 1:
                        if control.bo.board[x][y] != 0:
                            control.selected_pos = (x, y)
                            control.bo.set_enpassant((x, y))
                else:
                    pass

            
            if event.type == pygame.MOUSEBUTTONUP:
                m_x, m_y = event.pos
                if m_x < width:
                    x, y = get_square_onclick(m_x, m_y, w, h)
                    if control.selected_pos:
                        c, r = control.selected_pos
                        if control.mode == HUMAN_HUMAN:
                            if control.bo.move(control.selected_pos, (x, y)):
                                control.move_text = ""
                                promoted = True
                                # for promotion
                                if isinstance(control.bo.board[x][y], Pawn):
                                    if y == 0 or y == 7:
                                        promoted = await control.bo.promote(control.selected_pos, (x, y))
                                        control.bo.resize_pieces(w, h)
                                        control.bo.set_every_pos()
                                if promoted:
                                    todo_after_move()
                                    control.move_text = chr(97 + c) + str(8-r) + '-' + chr(97 + x) + str(8-y)

                        if control.mode == HUMAN_AI:
                            AI_move()


                    control.bo.set_every_pos()
                    control.selected_pos = ()

            if event.type == pygame.MOUSEMOTION:
                m_x, m_y = event.pos
                if control.selected_pos:
                    sp = control.selected_pos
                    if m_x > width:
                        m_x = width
                    img_x = m_x - w / 2
                    img_y = m_y - h / 2
                    control.bo.board[sp[0]][sp[1]].x = img_x
                    control.bo.board[sp[0]][sp[1]].y = img_y

            if event.type == pygame.VIDEORESIZE:
                control.bo.set_every_pos()

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    control.bo.undo()
                    control.bo.resize_pieces(w, h)
                    control.bo.set_every_pos()
                
                if event.key == pygame.K_RIGHT:
                    control.bo.redo()
                    control.bo.resize_pieces(w, h)
                    control.bo.set_every_pos()

                if event.key == pygame.K_SPACE:
                    if not control.selected_pos:
                        AI_move()
                        control.bo.set_every_pos()

        control.draw_window(win, width, height)
        await asyncio.sleep(0)  # let the browser run between frames


if __name__ == "__main__":
    asyncio.run(main())