
class Board():

    def __init__(self, init_board, *args, **kwargs):
        # Save tracking variables
        self.tiles = {}
        self.board = init_board
        self.b_size = len(init_board)
        
        
    def draw_pieces(self, board=None):
        #img = tk.PhotoImage(file="b1.png")  
        if board is not None:
            self.board = board

        
        for i in self.board:
            for j in i:
                print(j.piece, end=" ")
            print()
        print("------------------------------------")
        self.update()
