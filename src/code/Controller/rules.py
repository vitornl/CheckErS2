from ..Model.board import Board
from ..Model.piece import Piece
from ..Model.player import Player

class Rule:

    def __init__(self):
        self.board = Board()
        self.players, self.turn_player = self._set_players()
        self._init_board(self.board, self.players)

    def _set_players(self):
        p1 = Player('1', 'red')
        p2 = Player('2', 'blue')
        
        return (p1, p2), p1
   
    def _init_board(self, board, players):
        pieces = [Piece(players[0]) for i in range(12)]
        k = 0
        for i in range(5, 8):
            for j in range(0, 7, 2):
                board.add_piece(pieces[k], (j+i%2, i))
                k += 1
        players[0].set_pieces(pieces)

        pieces = [Piece(players[1]) for i in range(12)]
        k = 0
        for i in range(0, 3):
            for j in range(0, 7, 2):
                board.add_piece(pieces[k], (j+i%2, i))
                k += 1
        players[1].set_pieces(pieces)

    def move_piece(self, piece_position):
        pass
    
    '''
    def is_movable(self, board, new_position):
        if(self.orientation == 0 and #north
            new_position[1] > self.position[1] and #y
            (new_position[0] != self.position[0]-1 or #x
            new_position[0] != self.position[0]+1) and
            new_position != None): #empty
            return False

        elif(self.orientation == 1 and #north
            new_position[1] < self.position[1] and #y
            (new_position[0] != self.position[0]-1 or #x
            new_position[0] != self.position[0]+1) and
            new_position != None): #empty
            return False
        
        return True
    '''

    def eat_piece(self):
        pass

    def movable_piece(self, piece):
        pass

    def valid_moves(self, piece_position):
        pass

    def valid_pieces(self):
        pass

    def next_turn(self):
        if self.turn_player is self.players[0]:
            return self.players[1]
        return self.players[0]