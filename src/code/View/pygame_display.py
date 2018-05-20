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
    """
        Class for dealing with the pygame display

        Parameters
        ----------
        pywin: pygame window
    """
    def __init__(self):
        """
            Class builder, for starting pygame variables

            Returns
            -------
            A Pygame_Display class object
        """
        pygame.init()
        self.pywin = pygame.display.set_mode(_dim)

    def get_position(self):
        """
            Get the position selected by the mouse

            Returns
            -------
            A tuple representing a board position or a quit value
        """
        while True:
            var = self._event_listener(pygame.event.get())
            if var: return var

    def _draw_square(self, color, position):
        """
            Draw a square in the window

            Parameters
            ----------
            color: The square color
            position: the position to draw the square
        """
        x = position[0]*_tile_size
        y = position[1]*_tile_size
        rect = (x, y, _tile_size, _tile_size)
        pygame.draw.rect(self.pywin, color, rect)

    def _draw_piece(self, color, position, draught):
        """
            Draw a piece in the window

            Parameters
            ----------
            color: The piece color
            position: the position to draw the piece
            draught: Means if the piece is draught or not
        """
        x = (position[0] + 0.5)*_tile_size
        y = (position[1] + 0.5)*_tile_size
        pygame.draw.circle(self.pywin, color, (int(x), int(y)), _piece_size//2)
        if draught:
            pygame.draw.circle(self.pywin, _CENTER, (int(x), int(y)), _piece_size//4)

    def print_board(self, board, piece_selected, movement):
        """
            Draw the board in the window

            Parameters
            ----------
            board: board to be draw
            piece_selected: piece that is select to be played
            movement: the list of movement of the select piece
        """
        board_color = board_color_dic['classic']

        for i in range(8):
            for j in range(8):
                special = False
                piece_color = None
                draught = False
                square_color = None

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
        """
            Converts the mouse position to board position

            Parameters
            ----------
            x: colunn position of the mouse
            y: line position of the mouse

            Returns
            -------
            A tuple representing the board position
        """
        return x//_tile_size, y//_tile_size

    def _event_listener(self, events: pygame.event):
        """
            Deals with the events from pygame

            Parameters
            ----------
            events: list of events ocurring in the window
        """
        for event in events:
            if event.type == pygame.QUIT: return 1
            if event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                pos = self._screen_to_pos(mouse[0], mouse[1])
                print(pos)
                return tuple(pos)

    def quit(self):
        """
            Turn off pygame
        """
        pygame.quit()
