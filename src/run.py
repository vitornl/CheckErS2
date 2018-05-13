# coding=utf-8

from code.Controller.rules import Rule
from code.View.display import Display
from code.Controller.util import Util


def main():
    rules = Rule()
    Display.print_board_spaced(rules.board, None, None)

    print("Atenção!!! Digitar posições no formato: coluna linha\n")

    while (rules.win_condition()):
        possibilities = rules.get_all_possible_moves(rules.turn_player)
        piece_position = Util.string_to_int_tuple(input("Digite a peça a ser jogada: "))
        piece = rules.board.get_piece(piece_position)
        if piece in possibilities.keys():
            for p in possibilities[piece]:
                print(p.get_position())
            Display.print_board_spaced(rules.board, piece, possibilities)
        
            movement_position = Util.string_to_int_tuple(input("Digite a posição do movimento da peça: "))
            movement = None

            for mov in possibilities[piece]:
                if mov.get_position() == movement_position:
                    #Se entrou aqui significa que achou um movimento possível com aquela posição
                    movement = mov
                    break

            if movement != None:
                rules.move_piece(piece, movement)
                rules.next_turn()
                print("Jogada realizada com sucesso.")
            
            else:
                print("Movimento impossível.")
        else:
            print("Selecione uma peça sua que tenha movimentos possíveis.")

        rules.check_draughts(piece)

        Display.print_board_spaced(rules.board, None, None)     

if __name__ == "__main__":
    main()
