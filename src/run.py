from code.Controller.rules import Rule
from code.View.display import Display
from code.Controller.util import Util

def main():
    rules = Rule()
    Display.print_board(rules.board.board)
    print()
    print("Atenção!!! Digitar jogada no formato: coluna_atual linha_atual coluna_nova linha_nova\n")
    
    while (True):
        text_play = input("Digite a próxima jogada: ")
        play = Util.string_to_int_list(text_play)
        
        while (len(play) == 0):
            text_play = input("Erro na digitação! Digite corretamente a próximada jogada: ")
            play = Util.string_to_int_list(text_play)
            
        rules.move_piece((play[0], play[1]), (play[2], play[3]))
        print()
        Display.print_board(rules.board.board)
        print()
    
if __name__ == "__main__":
    main()
