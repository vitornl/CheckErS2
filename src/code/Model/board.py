class Board:
    """
        Class for dealing with the board

        Parameters
        ----------
        board: game board, matrix where each element is None or a piece
    """
    def __init__(self):
        """
            Class builder

            Returns
            -------
            A Board class object
        """
        self.board = self._new_board()

    def _new_board(self):
        """
            Start-up a new board

            Returns
            -------
            A matrix where every None
        """
        board = [[None] * 8 for i in range(8)]
        
        return board

    def get_piece(self, position):
        """
            Getter for a piece

            Parameters
            ----------
            position: position of the expected piece

            Returns
            -------
            A piece or None
        """
        if position[0]<0 or position[0]>7 or position[1]<0 or position[1]>7:
            return None
        return self.board[position[0]][position[1]]

    def add_piece(self, piece, position):
        """
            Add a piece in the board

            Parameters
            ----------
            piece: the piece that is going to be placed in the board
            position: position to place the piece
        """
        self.board[position[0]][position[1]] = piece
        piece.set_position(position)

    def move_piece(self, piece, position):
        """
            Move a piece in the board

            Parameters
            ----------
            piece: the piece that is going to be moved in the board
            position: position to place the piece
        """
        self.remove_piece(piece)
        self.add_piece(piece, position)

    def remove_piece(self, piece):
        """
            Remove a piece from the board

            Parameters
            ----------
            piece: the piece that is going to be removed from the board
        """
        self.board[piece.position[0]][piece.position[1]] = None
        piece.set_position((None, None))