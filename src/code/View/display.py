class Display:

    @staticmethod
    def print_board(board, piece, possibilities):
        for i in range(len(board.board[0])):
            for j in range(len(board.board[0])):
                # Casos de hover, S para para peça selecionada, X para casa jogável
                if piece is not None:
                    if board.get_piece((j, i)) == piece:
                        print("S", end=" ")
                        continue
                    elif (j, i) in possibilities[piece]:
                        print('X', end=" ")
                        continue

                if(board.board[j][i] != None):
                    print(board.board[j][i].player.name, end=" ")
                else:
                    print("0", end=" ")

            print()

    @staticmethod
    def print_board_spaced(board, piece, possibilities):
        print()
        Display.print_board(board, piece, possibilities)
        print()
