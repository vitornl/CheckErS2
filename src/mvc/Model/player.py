from .piece import Piece

class Player:
    """
        Class for dealing with the player

        Parameters
        ----------
        name: name of the player
        color: color of pieces (red or blue)
        side: position of the player in the board, -1 the player is the upper side, 1 player is in bottom side
        pieces: list playable pieces of the player
    """
    def __init__(self, name, color, side):
        """
            Class builder

            Parameters
            ----------
            player: player owner of the piece

            Returns
            -------
            A Piece class object
        """
        self.name = name
        self.color = color
        self.side = side
        self.pieces = []
        self.draw_turns = 0

    def set_pieces(self, pieces):
        """
            Set the valid pieces list to the player

            Parameters
            ----------
            pieces: The list of valid pieces to be assigned to the player
        """
        self.pieces = pieces
    
    def remove_piece(self, piece):
        """
            Class builder

            Parameters
            ----------
            piece: piece to be removed
        """
        self.pieces.remove(piece)

          self.pieces.remove(piece)

    def get_qty_draughts(self):
        qty = 0
        for piece in self.pieces:
            if piece.is_draughts:
                qty += 1
        return qty