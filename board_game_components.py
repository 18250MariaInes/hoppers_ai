class Board():

    def __init__(self, init_board, *args, **kwargs):
        # Save tracking variables
        self.tiles = {}
        self.board = init_board
        self.b_size = len(init_board)
        

class Tile():

    def __init__(self, tile=0, piece=0, row=0, col=0):
        self.tile = tile
        self.piece = piece

        self.row = row
        self.col = col
        self.loc = (row, col)


    def __str__(self):
        return chr(self.loc[1] + 97) + str(self.loc[0] + 1)

    def __repr__(self):
        return chr(self.loc[1] + 97) + str(self.loc[0] + 1)