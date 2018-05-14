class Movement:
    """
        Class that deals with the movement routing
    """
    def __init__(self, piece, destiny):
        """
            Class builder

            Parameters
            ----------
            piece: Piece that is going to move
            destiny: New position of the piece

            Returns
            -------
            A Movement class object
        """
        self.piece = piece
        self.destiny = []
        self.destiny.append(destiny)
        self.eliminated = []

    def get_piece(self):
        """
            Getter for piece

            Returns
            -------
            The piece that is in movement
        """
        return self.piece

    def get_movement(self):
        """
            Getter for first movement

            Returns
            -------
            The destiny position
        """
        return self.destiny.pop()

    def get_eliminateds(self):
        """
            Getter for eliminated pieces list

            Returns
            -------
            The list of eliminated pieces
        """
        return self.eliminated

    def add_new_destiny(self, location):
        """
            Add a new destiny for the piece

            Parameters
            ----------
            location: New position of the piece

            Returns
            -------
            Bool meaning if is a new position or not
        """
        if location in self.destiny:
            return False
        self.destiny.append(location)
        return True

    def add_new_elimination(self, piece):
        """
            Add a new eliminated piece

            Parameters
            ----------
            piece: New piece to be removed
        """
        self.eliminated.append(piece)