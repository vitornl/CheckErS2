# coding=utf-8
from ..Model.movement import Movement

class Display:

    @staticmethod
    def print_board(board, piece_selected, possibilities):
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
                    for mov in possibilities[piece_selected]:
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
                    print("0", end=" ")

            print()

    @staticmethod
    def print_board_spaced(board, piece_selected, possibilities):
        print()
        Display.print_board(board, piece_selected, possibilities)
        print()
