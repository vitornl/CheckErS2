# coding=utf-8

from code.Controller.rules import Rule
from code.View.display import Display
from code.Controller.util import Util


def main():
    rules = Rule()

    print("Atenção!!! Digitar posições no formato: coluna linha\n")

    while (rules.win_condition()):
        Display.print_board_spaced(rules.board, None, None)

        possibilities = rules.get_all_possible_moves(rules.turn_player)
        print("--- TURNO: Jogador {} ---".format(rules.turn_player.name))
        piece_position = Util.string_to_int_tuple(input("Digite a peça a ser jogada: "))
        piece = rules.board.get_piece(piece_position)
        if piece in possibilities.keys() and len(possibilities[piece]) != 0:

            path = possibilities[piece]

            while len(path) != 0:
                movement = []
                while len(movement) == 0:
                    Display.print_board_spaced(rules.board, piece, path)
                
                    movement_position = Util.string_to_int_tuple(input("Digite a posição do movimento da peça: "))

                    for mov in path:
                        if mov.get_movement() == movement_position:
                            #Se entrou aqui significa que achou um movimento possível com aquela posição
                            movement.append(mov)

                    if len(movement) == 0:
                        print("Posição inválida.")
                rules.move_piece(piece, movement_position)

                for mov in movement:
                    mov.next_movement()
                
                if (len(movement) == 1) and (movement[0].get_movement() == None):
                    path = []
                    rules.eat_pieces(movement[0])
                    rules.check_draughts(piece)
                    rules.next_turn()
                    print("Jogada realizada com sucesso.")
                else:
                    path = movement
        else:
            print("Selecione uma peça sua que tenha movimentos possíveis.")

if __name__ == "__main__":
    main()
