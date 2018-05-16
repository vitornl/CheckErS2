# coding=utf-8
from ..Model.movement import Movement

class Console_Display:

    def _print_board(self, board, piece_selected, movement):
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
                    if not piece.is_draughts:
                        print(board.board[j][i].player.name, end=" ")
                    else:
                        print(str.capitalize(board.board[j][i].player.name), end=" ")
                else:
                    print("_", end=" ")

            print()

    def print_board(self, board, piece_selected, possibilities):
        print()
        self._print_board(board, piece_selected, possibilities)
        print()

    def get_piece_position(self):
        string = input()
        aux = string.split(" ")
        if len(aux) != 2:
            return 1
        tup = tuple(map(int, aux))
        return tup

    def quit(self):
        pass
