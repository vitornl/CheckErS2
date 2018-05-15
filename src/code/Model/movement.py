class Movement:
    """
        Class that deals with the movement routing

        Parameters
        ----------
        piece: piece in movement
        destiny: the list of position of the piece
        eliminated: the list of pieces jumped, that is going to be removed
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

    def copy_movement(self):
        """
            Copy a movement to a new object

            Returns
            -------
            A new Movement class object
        """
        resp = Movement(self.piece, self.destiny[0])
        dest = self.destiny[1:]
        for pos in dest:
            resp.add_destiny(pos)
        for piece in self.eliminated:
            resp.add_elimination(piece)
        return resp


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
            The destiny position or None
        """
        if len(self.destiny)==0:
            return None
        else:
            return tuple(self.destiny[0])

    def get_last_movement(self):
        """
            Getter for last movement

            Returns
            -------
            The destiny position or None
        """
        if len(self.destiny)==0:
            return None
        else:
            return tuple(self.destiny[-1])

    def next_movement(self):
        """
            Remove the first movement
        """
        self.destiny.remove(self.destiny[0])

    def get_eliminateds(self):
        """
            Getter for eliminated pieces list

            Returns
            -------
            The list of eliminated pieces
        """
        return self.eliminated

    def check_destiny(self, location):
        """
            Checks if a position is already in the list

            Parameters
            ----------
            location: the location to be evaluated

            Returns
            -------
            True: Element in the list
            False: New element
        """
        if location in self.destiny:
            return True
        return False
    
    def check_elimination(self, piece):
        """
            Checks if a piece is already in the list

            Parameters
            ----------
            piece: the piece to be evaluated

            Returns
            -------
            True: Element in the list
            False: New element
        """
        if piece in self.eliminated:
            return True
        return False

    def add_destiny(self, location):
        """
            Add a new destiny for the piece

            Parameters
            ----------
            location: New position of the piece
        """
        self.destiny.append(location)

    def add_elimination(self, piece):
        """
            Add a new eliminated piece

            Parameters
            ----------
            piece: New piece to be removed
        """
        self.eliminated.append(piece)