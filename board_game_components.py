"""
María Inés Vásquez Figueroa
18250
AI-ba player for Hopper board game
Board game components
"""

class Board():

    def __init__(self, init_board, *args, **kwargs):
        # Save tracking variables
        self.tiles = {}
        self.board = init_board
        self.b_size = len(init_board)
        

class Bunny():

    def __init__(self, tile=0, piece=0, row=0, col=0):
        self.tile = tile
        self.piece = piece

        self.row = row
        self.column = col
        self.coord = (row, col)


    def __str__(self):
        return chr(self.coord[1] + 97) + str(self.coord[0] + 1)

    def __repr__(self):
        return chr(self.coord[1] + 97) + str(self.coord[0] + 1)