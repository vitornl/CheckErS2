# coding=utf-8

from code.Controller.rules import Rule
from code.View.display import Display
from code.Controller.util import Util


def main():
    rules = Rule()
    Display.print_board_spaced(rules.board, None, None)

    print("Atenção!!! Digitar posições no formato: coluna linha\n")

    while (True):
        possibilities = rules.get_possibilities()

        piece_position = Util.string_to_int_tuple(input("Digite a peça a ser jogada: "))
        piece = rules.board.get_piece(piece_position)

        if piece in possibilities.keys():
            Display.print_board_spaced(rules.board, piece, possibilities)

            movement_position = Util.string_to_int_tuple(input("Digite a posição do movimento da peça: "))

            if (movement_position in possibilities[piece]):
                rules.move_piece(piece_position, movement_position)
                print("Jogada realizada com sucesso.")
            else:
                print("Movimento impossível.")
        else:
            print("Selecione uma peça sua que tenha movimentos possíveis.")

        Display.print_board_spaced(rules.board, None, None)


if __name__ == "__main__":
    main()
