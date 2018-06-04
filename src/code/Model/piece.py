from ..Model.board import Board

class Piece:
    """
        Class for dealing with the piece

        Parameters
        ----------
        player: player owner of the piece
        is_draught: bool, meaning if the piece is draught of not
        position: position of the piece in the board
    """
    def __init__(self, player):
        """
            Class builder

            Parameters
            ----------
            player: player owner of the piece

            Returns
            -------
            A Piece class object
        """
        self.player = player
        self.is_draughts = False
        self.position = (None, None)
    
    def turn_draughts(self):
        """
            Set a normal piece to draught
        """
        self.is_draughts = True

    def get_position(self):
        """
            Getter for position

            Returns
            -------
            The piece position in the board
        """
        return self.position

    def set_position(self, position):
        """
            Set the piece position

            Parameters
            ----------
            position: position of where the piece is in the board
        """
        self.position = tuple(position)
