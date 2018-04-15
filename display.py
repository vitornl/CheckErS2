import itertools
import pygame

BLACK = pygame.Color('black')
WHITE = pygame.Color('white')
RED = pygame.Color('red')
BLUE = pygame.Color('blue')
GOLD = pygame.Color('gold')

class Display:

    def __init__(self, size, title):
        self.title = title
        self.width, self.height = size
        self.tile_w = int(self.width / 8)
        self.tile_h = int(self.height / 8)
        self.circle_r = int(self.tile_h / 2) if self.tile_h < self.tile_w else int(self.tile_h / 2)
        self.screen = pygame.display.set_mode([self.width, self.height])
        pygame.display.set_caption(self.title)

    def draw_board(self, board):
        colors = itertools.cycle((BLACK, WHITE))
        i = 0
        for x in range(0, self.width, self.tile_w):
            j = 0
            for y in range(0, self.height, self.tile_h):
                rect = (x, y, self.tile_w, self.tile_h)
                pygame.draw.rect(self.screen, next(colors), rect)
                if(board[i][j] != None):
                    piece = board[i][j]
                    color = pygame.Color(piece.player.color)
                    pos = (int(x + self.tile_w/2), int(y + self.tile_h/2))
                    pygame.draw.circle(self.screen, color, pos, self.circle_r)
                j += 1
            i += 1
            next(colors)
    
    def get_board_position(self, event):
        mouse = pygame.mouse.get_pos()
          
        return self._identify_board_position(mouse)

    def _identify_board_position(self, mouse_position):
        return (int(mouse_position[0]/self.tile_w), 
        int(mouse_position[1]/self.tile_h))

    def highlight_piece(self, piece):
        pos = self._identify_display_position(piece.position)
        rect = (pos[0], pos[1], self.tile_w, self.tile_h)
        pygame.draw.rect(self.screen, GOLD, rect)

    def _identify_display_position(self, board_position):

        return (board_position[0]*self.tile_w, board_position[1]*self.tile_h)