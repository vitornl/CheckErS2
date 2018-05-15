from .piece import Piece

class Player:
    def __init__(self, name, side):
        self.name = name
        self.side = side
        self.pieces = []

    def set_pieces(self, pieces):
        self.pieces = pieces
    
    def remove_piece(self, position):
        for piece in self.pieces:
           if piece.get_position()[0] == None:
               self.pieces.remove(piece)
               break

    def move_piece(self, old_position, new_position):
        for piece in self.pieces:
            if piece.get_position() == old_position:
                piece.set_position(new_position)
                break