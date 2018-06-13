# coding=utf-8
from ..Model.movement import Movement

player_color = { 'red': 'r', 'blue': 'b' }

class Console_Display:
    """
        Class for dealing with the console display
    """

    def print_board(self, board, piece_selected, movement):
        """
            Draw the board in the console

            Parameters
            ----------
            board: board to be draw
            piece_selected: piece that is select to be played
            movement: the list of movement of the select piece
        """
        print()
        print(" ", end=" ")
        for i in range(len(board.board[0])): #header
            print(i, end=" ")
        print("")
        for i in range(len(board.board[0])):
            print(i, end=" ")
            for j in range(len(board.board[0])):
                # Casos de hover, S para para peça selecionada, X para casa jogável
                if piece_selected is not None:
                    possMovs = []
                    for mov in movement:
                        possMovs.append(mov.get_movement())

                    if board.get_piece((j, i)) == piece_selected:
                        print("S", end=" ")
                        continue
                    elif (j, i) in possMovs:
                        print('X', end=" ")
                        continue

                if(board.board[j][i] != None):
                    piece = board.get_piece((j, i))
                    color = player_color[board.board[j][i].player.color]
                    if not piece.is_draughts:
                        print(color, end=" ")
                    else:
                        print(str.capitalize(color), end=" ")
                else:
                    print("_", end=" ")

            print()
        print()

    def get_position(self):
        """
            Get the position writed in the console

            Returns
            -------
            A tuple representing a board position or a quit value
        """
        string = input()
        aux = string.split(" ")
        if len(aux) != 2:
            return 1
        tup = tuple(map(int, aux))
        return tup

    def quit(self):
        """
            Do noting
        """
        pass
