class Display:

    @staticmethod
    def print_board(board):
        for i in range(len(board[0])):
            for j in range(len(board[0])):
                if(board[j][i] != None):
                    print(board[j][i].player.name, end=" ")
                else:
                    print("0", end=" ")
            print()
