import pygame

from .ctx import *
from .table import *
from .piece import *

class GameWindow():

    selected_piece = False, -1

    def __init__(self, pywin: pygame.Surface):
        self.pywin = pywin
        self.table = Table(pywin)

    def event_listener(self, events: pygame.event):
        for event in events:
            if event.type == pygame.QUIT: return 1
            if event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                pos = screen_to_pos(mouse[0], mouse[1])
                print(pos)
                if(self.selected_piece[0]):
                    self.table.player1[self.selected_piece[1]].move(pos[0], pos[1])
                    self.selected_piece = False, -1
                else:
                    for piece in self.table.player1:
                        # print("x = {} = {}, y = {} = {}".format(piece.x, pos[0], piece.y, pos[1]))
                        if(piece.compare(pos[0], pos[1])):
                            # print("match find")
                            self.selected_piece = True, self.table.player1.index(piece)
                    # self.table.player1[-2].move(1, 1)
                    return 0

    def game_loop(self):
        clock = pygame.time.Clock()
        while True:
            var = self.event_listener(pygame.event.get())
            if var: break

            self.update_visible()
            pygame.display.update()

    def update_visible(self):
        self.table.place()
        self.table.update_players()

    def run(self):
        self.game_loop()
        pygame.quit()