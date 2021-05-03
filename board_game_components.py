"""
María Inés Vásquez Figueroa
18250
AI-ba player for Hopper board game
Board game components
"""
#clase del tablero de juego
class Board():

    def __init__(self, init_board, *args, **kwargs):
        # Save tracking variables
        self.tiles = {}
        self.board = init_board
        self.b_size = len(init_board)


    #inicializar el tablero
    def initialize_game_board(size_of_board):
        board = [[None] * size_of_board for _ in range(size_of_board)]
        
        for row in range(size_of_board):
            for col in range(size_of_board):

                if row + col < 5:
                    element = Bunny(2, 2, row, col)
                elif 1 + row + col > 2 * (size_of_board - 3):
                    
                    element = Bunny(1, 1, row, col)
                else:
                    element = Bunny(0, 0, row, col)
                board[row][col] = element
        
        return board
    #calcular área de victoria
    def set_gamer_territory(board):
        aiba_zone = [a for row in board
                        for a in row if a.tile == 2]
        human_zone = [h for row in board
                        for h in row if h.tile == 1]
        return aiba_zone, human_zone

        
#clase de las piezas que son conejos
class Bunny():
    def __init__(self, tile=0, piece=0, row=0, col=0):
        self.tile = tile
        self.row = row
        self.piece = piece
        self.column = col
        self.coord = (row, col)
