"""
María Inés Vásquez Figueroa
18250
AI-ba player for Hopper game board
AI player
"""

# Python Standard Library imports
import time
import math

# Custom module imports
from board_game_components import Board, Bunny


class Ai_player():

    def __init__(self):
        self.b_size = 10
        self.t_limit = 20
        
        # Create initial board
        board = [[None] * self.b_size for _ in range(self.b_size)]
        
        for row in range(self.b_size):
            for col in range(self.b_size):

                if row + col < 5:
                    element = Bunny(2, 2, row, col)
                elif 1 + row + col > 2 * (self.b_size - 3):
                    
                    element = Bunny(1, 1, row, col)
                else:
                    element = Bunny(0, 0, row, col)

                board[row][col] = element
        #print(board)
        # Save member variables
        self.c_player = 2
        self.board = board
        self.current_player = 1
        self.valid_moves = []
        self.computing = False
        self.total_plies = 0

        self.ply_depth = 3
        #self.ab_enabled = True

        self.r_goals = [t for row in board
                        for t in row if t.tile == 2]
        print(self.r_goals)
        self.g_goals = [t for row in board
                        for t in row if t.tile == 1]


        # Print initial program info
        print("Hoppers game with AI by María Inés Vásquez")
        print("Playing against: AI-ba")
        """print("Turn time limit:", self.t_limit)
        print("Max ply depth:", self.ply_depth)"""
        print()


    def minimax(self, depth, player_to_max, max_time, a=float("-inf"),
                b=float("inf"), maxing=True, prunes=0, boards=0):

        # Bottomed out base case
        if depth == 0 or self.win_analyzer() or time.time() > max_time:
            return self.utility_distance(player_to_max), None, prunes, boards

        # Setup initial variables and find moves
        best_move = None
        if maxing:
            best_val = float("-inf")
            moves = self.get_next_moves(player_to_max)
        else:
            best_val = float("inf")
            moves = self.get_next_moves((2
                    if player_to_max == 1 else 1))
        # For each move
        for move in moves:
            for to in move["to"]:
                # Bail out when we're out of time
                if time.time() > max_time:
                    return best_val, best_move, prunes, boards

                # Move piece to the move outlined
                piece = move["from"].piece
                move["from"].piece = 0
                to.piece = piece
                boards += 1

                # Recursively call self
                #se vuelve a llamar de acuerdo a la profundidad programada para poder ver la mejor jugada a largo plazo
                val, _, new_prunes, new_boards = self.minimax(depth - 1,
                    player_to_max, max_time, a, b, not maxing, prunes, boards)
                prunes = new_prunes
                boards = new_boards

                # Move the piece back
                to.piece = 0
                move["from"].piece = piece

                if maxing and val > best_val:
                    best_val = val
                    best_move = (move["from"].coord, to.coord)
                    a = max(a, val)

                if not maxing and val < best_val:
                    best_val = val
                    best_move = (move["from"].coord, to.coord)
                    b = min(b, val)

                if b <= a:
                    return best_val, best_move, prunes + 1, boards

        return best_val, best_move, prunes, boards

    

    def get_next_moves(self, player=1):
        moves = []  # All possible moves
        for col in range(self.b_size):
            for row in range(self.b_size):

                curr_tile = self.board[row][col]

                # Skip board elements that are not the current player
                if curr_tile.piece != player:
                    continue

                move = {
                    "from": curr_tile,
                    "to": self.get_valid_moves(curr_tile, player)
                }
                moves.append(move)

        return moves

    def get_valid_moves(self, tile, player, moves=None, adj=True):

        if moves is None:
            moves = []

        row = tile.coord[0]
        col = tile.coord[1]

        # List of valid tile types to move to
        valid_tiles = [0, 1, 2]

        # Find and save immediately adjacent moves
        for col_delta in range(-1, 2):
            for row_delta in range(-1, 2):

                # Check adjacent tiles

                new_row = row + row_delta
                new_col = col + col_delta

                # Skip checking degenerate values
                #para revisar que no me estoy saliendo del tablero
                if ((new_row == row and new_col == col) or
                    new_row < 0 or new_col < 0 or
                    new_row >= self.b_size or new_col >= self.b_size):
                    continue

                # Handle moves out of/in to goals
                new_tile = self.board[new_row][new_col]
                
                if new_tile.piece == 0:
                    if adj:  # Don't consider adjacent on subsequent calls 
                    #si hay un movimiento para seguirle dando
                        moves.append(new_tile)
                    continue

                # Check jump tiles

                new_row = new_row + row_delta
                new_col = new_col + col_delta

                # Skip checking degenerate values
                if (new_row < 0 or new_col < 0 or
                    new_row >= self.b_size or new_col >= self.b_size):
                    continue

                # Handle returning moves and moves out of/in to goals
                new_tile = self.board[new_row][new_col] #para no poder regresar a mi área 
                if new_tile in moves or (new_tile.tile not in valid_tiles):
                    continue

                if new_tile.piece == 0:
                    moves.insert(0, new_tile)  # Prioritize jumps
                    self.get_valid_moves(new_tile, player, moves, False)

        return moves

    def move_piece(self, from_tile, to_tile):

        # Handle trying to move a non-existant piece and moving into a piece
        if from_tile.piece == 0 or to_tile.piece != 0:
            print("Movimiento inválido, vuelva a ingresar valores")
            return False

        # Move piece
        to_tile.piece = from_tile.piece
        from_tile.piece = 0
        self.total_plies += 1


    def win_analyzer(self):

        if all(g.piece == 1 for g in self.r_goals):
            return 1
        elif all(g.piece == 2 for g in self.g_goals):
            return 2
        else:
            return None


    def utility_distance(self, player):

        def point_distance(p0, p1):
            #IDEA: CALCULAR DISTANCIA MÁS CORTA AL ÁREA DE META
            
            """print("coord: ",p1,p0)
            if (player ==2):
                p1 = (9,9)
            else:
                p1 = (0,0)
            print(math.sqrt((p1[0] - p0[0])**2 + (p1[1] - p0[1])**2))
            print("----------------")"""
            return math.sqrt((p1[0] - p0[0])**2 + (p1[1] - p0[1])**2)

        value = 0
        
        for col in range(self.b_size):
            for row in range(self.b_size):

                tile = self.board[row][col]

                if tile.piece == 1:
                    distances = []
                    for g in self.r_goals:
                        if g.piece != 1:
                            distances.append(point_distance(tile.coord, g.coord))
                    """distances1 = [point_distance(tile.coord, g.coord) for g in
                                 self.r_goals if g.piece != 1]"""
                    value -= max(distances) if len(distances) else -50

                elif tile.piece == 2:
                    distances = []
                    for g in self.g_goals:
                        if g.piece != 2:
                            distances.append(point_distance(tile.coord, g.coord))

                    """distances1 = [point_distance(tile.coord, g.coord) for g in
                                 self.g_goals if g.piece != 2]"""
                    value += max(distances) if len(distances) else -50

        if player == 2:
            value *= -1
        #print(value)
        return value
    
    def AIba_turn(self):
        # Print out search information
        current_turn = (self.total_plies // 2) + 1
        print("Turn de Al-ba")
        print("--------------------------")
        print("Calculando ...")

        # self.board_view.set_status("Computing next move...")
        self.computing = True
        max_time = time.time() + self.t_limit

        # Execute minimax search
        start = time.time()
        _, move, prunes, boards = self.minimax(self.ply_depth,
            self.c_player, max_time)
        end = time.time()

        """MOVE ES EL MOVIMIENTO DE AI"""
        print("Al-ba se ha movido de "+str(move[0])+" a "+str(move[1]))
        move_from = self.board[move[0][0]][move[0][1]]
        move_to = self.board[move[1][0]][move[1][1]]
        self.move_piece(move_from, move_to)

        winner = self.win_analyzer()
        if winner:
            print("AI-BA HA GANADO!")
            self.current_player = None

        else:  # Toggle the current player
            self.current_player = (2
                if self.current_player == 1 else 1)

        self.computing = False
        print()
    
    #mi jugada
    def human_player_move(self):
        current_turn = (self.total_plies // 2) + 1
        validation = True
        print("¡Tu turno!")
        print("----------------------------------")

        move_from_row = int(input("Ingrese fila de la pieza a mover:"))
        move_from_col = int(input("Ingrese columna de la pieza a mover :"))

        move_to_row = int(input("Ingrese fila a donde desea moverla:"))
        move_to_col = int(input("Ingrese columna a donde desea moverla :"))
        
        move_from = self.board[move_from_row][move_from_col]
        self.valid_moves = self.get_valid_moves(move_from,1)

        move_to = self.board[move_to_row][move_to_col]
        print("Te has movido de ("+str(move_from_row)+","+str(move_from_col)+") a ("+str(move_to_row)+","+str(move_to_col)+")")
        if (move_to not in self.valid_moves):
            print("Ese movimiento no es válido")
            return
        else:
            validation = self.move_piece(move_from, move_to)

        winner = self.win_analyzer()
        if winner:
            print("LE HAS GANADO A AIBA!")
            self.current_player = None
        elif (validation==False):
            self.human_player_move()
        elif self.c_player is not None:
            self.AIba_turn()
        else:  # Toggle the current player
            self.current_player = (2
                if self.current_player == 1 else 1)
        

        

            
    
