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
        for i in range(0, 3):
            for j in range(0, 7, 2):
                board.add_piece(pieces[k], (j+i%2, i))
                k += 1
        players[0].set_pieces(pieces)

        pieces = [Piece(players[1]) for i in range(12)]
        k = 0
        for i in range(5, 8):
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
        neighborhood = self.board.get_surroundings(piece)
        for neighbor in neighborhood:
            if neighbor is None:
                return True
            if not neighbor.player is piece.player:
                return True
        return False
        
    def valid_moves(self, piece_position):
        pass

    def valid_pieces(self):
        pass

    def _other_player(self, player):
        if player is self.players[0]:
            return self.players[1]
        return self.players[0]

    def win_condition(self):
        for player in self.players:
            if len(player.pieces) > 0:
                for piece in player.pieces:
                    if self.movable_piece(piece):
                        return None
            return self._other_player(player)

    def next_turn(self):
        self.turn_player = self._other_player(self.turn_player)