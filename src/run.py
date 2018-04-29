from code.Controller.rules import Rule
from code.View.display import Display

def main():
    rules = Rule()
    Display.print_board(rules.board.board)
    print()
    
if __name__ == "__main__":
    main()