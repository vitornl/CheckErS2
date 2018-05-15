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

    def copy_movement(self):
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
        if location in self.destiny:
            return True
        return False
    
    def check_elimination(self, piece):
        if piece in self.eliminated:
            return True
        return False

    def add_destiny(self, location):
        """
            Add a new destiny for the piece

            Parameters
            ----------
            location: New position of the piece

            Returns
            -------
            Bool meaning if is a new position or not
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