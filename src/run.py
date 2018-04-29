from code.Model.Table import Table
from code.Model.Piece import Piece

t = Table()

for i in range(len(t.table[0])):
    for j in range(len(t.table[0])):
        try:
            c = t.select_piece((i, j)).color
            print(c,end=" ")
        except:
            print("0", end=" ")

    print ()