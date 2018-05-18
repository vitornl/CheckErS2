import pygame

_BLACK = pygame.Color('black')
_WHITE = pygame.Color('white')
_BLUE = pygame.Color('blue')
_RED = pygame.Color('red')
_BROWN = (92, 51, 23, 255)
_LWOOD = (233, 194, 166, 255)
_HOVER = pygame.Color('yellow')
_SELECTED = pygame.Color('darkseagreen')
_CENTER = pygame.Color('green')

board_color_dic = { 'classic': [_BLACK, _WHITE], 'wood': [_BROWN, _LWOOD] }

player_color = { 'red': _RED, 'blue': _BLUE }

_tile_size = 75
_piece_size = 72
_size = 8*_tile_size
_dim = _width, _height = _size, _size

class Pygame_Display:

    def __init__(self):
        pygame.init()
        self.pywin = pygame.display.set_mode(_dim)

    def get_position(self):
        while True:
            var = self._event_listener(pygame.event.get())
            if var: return var

    def _draw_square(self, color, position):
        x = position[0]*_tile_size
        y = position[1]*_tile_size
        rect = (x, y, _tile_size, _tile_size)
        pygame.draw.rect(self.pywin, color, rect)

    def _draw_piece(self, color, position, draught):
        x = (position[0] + 0.5)*_tile_size
        y = (position[1] + 0.5)*_tile_size
        pygame.draw.circle(self.pywin, color, (int(x), int(y)), _piece_size//2)
        if draught:
            pygame.draw.circle(self.pywin, _CENTER, (int(x), int(y)), _piece_size//4)

    def print_board(self, board, piece_selected, movement):
        board_color = board_color_dic['wood']

        for i in range(8):
            for j in range(8):
                special = False
                piece_color = None
                draught = False
                square_color = None
                # Casos de hover, S para para peça selecionada, X para casa jogável
                if piece_selected is not None:
                    possMovs = []
                    for mov in movement:
                        possMovs.append(mov.get_movement())

                    if (j, i) in possMovs:
                        square_color = _HOVER
                        special = True

                    elif board.get_piece((j, i)) == piece_selected:
                        piece_color = _SELECTED
                        draught = piece_selected.is_draughts
                        special = True

                if (board.board[j][i] != None) and not special:
                    piece = board.get_piece((j, i))
                    piece_color = player_color[board.board[j][i].player.color]
                    draught = piece.is_draughts

                if square_color == None:
                    square_color = board_color[(i+j)%2]
                self._draw_square(square_color, (j, i))
                if piece_color != None:
                    self._draw_piece(piece_color, (j, i), draught)
                    
        pygame.display.update()
                

    def _screen_to_pos(self, x, y):
        return x//_tile_size, y//_tile_size

    def _event_listener(self, events: pygame.event):
        for event in events:
            if event.type == pygame.QUIT: return 1
            if event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                pos = self._screen_to_pos(mouse[0], mouse[1])
                print(pos)
                return tuple(pos)

    def quit(self):
        pygame.quit()