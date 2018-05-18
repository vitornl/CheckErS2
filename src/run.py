# coding=utf-8
import sys

from code.Controller.rules import Rule
from code.View.pygame_display import Pygame_Display
from code.View.console_display import Console_Display


def main():
    if len(sys.argv) != 2:
        print("Invalid Input")
        return

    rules = Rule()
    display = None

    if sys.argv[1] == "pygame":
        display = Pygame_Display()
    elif sys.argv[1] == "console":
        display = Console_Display()
    else:
        return

    possibilities = rules.get_all_possible_moves(rules.turn_player)
    print("Atenção!!! Digitar posições no formato: coluna linha\n")

    while rules.who_won(possibilities) is None:

        display.print_board(rules.board, None, None)

        print("--- TURNO: Jogador {} ---".format(rules.turn_player.name))

        print("Digite a peça a ser jogada: ", end='', flush=True)
        piece_position = display.get_position()
        if type(piece_position) != tuple:
            display.quit()
            return
        piece = rules.board.get_piece(piece_position)
        if piece in possibilities.keys():

            path = possibilities[piece]

            while len(path) != 0:
                movement = []
                while len(movement) == 0:
                    display.print_board(rules.board, piece, path)
                
                    print("Digite a posição do movimento da peça: ", end='', flush=True)
                    movement_position = display.get_position()
                    if type(piece_position) != tuple:
                        display.quit()
                        return

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

        possibilities = rules.get_all_possible_moves(rules.turn_player)

    display.quit()
    print("Jogador {} ganhou!".format(rules.who_won(possibilities).name))

if __name__ == "__main__":
    main()
