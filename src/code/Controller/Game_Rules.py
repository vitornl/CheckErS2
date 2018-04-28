import itertools
from ..Model.Table import Table
from ..Model.Piece import Piece
from ..Model.Square import Square
from ..ctx import piece_color_1, piece_color_2

class Game_Rules:
    __slots__ = ('board', 'turn_player')
    def __init__(self):
        self.board = Table()
        self.turn_player = itertools.cycle([piece_color_1, piece_color_2])

    def move_piece(self, piece_position: list):
        pass
    
    def eat_piece(self):
        pass

    def movable_piece(self, piece: Piece) -> bool:#private
        for x in [-1, 1]:
            for y in [-1, 1]:
                square = self.board.select_square([piece.get_position()[0] + x, piece.get_position()[1] + y])
                if not square.has_piece():
                    return True
                else:
                    other_piece = self.board.select_piece([piece.get_position()[0] + x, piece.get_position()[1] + y])
                    if not other_piece.color == piece.color:
                        return True
        return False

    def valid_moves(self, piece_position: list) -> list:
        pass

    def valid_pieces(self) -> list:
        pass

    def next_turn(self):
        pass