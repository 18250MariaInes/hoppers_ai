"""
María Inés Vásquez Figueroa
18250
AI-ba player for Hopper game board
AI player
"""

import time
import math
from xml.dom import minidom
import os 
from board_game_components import Board, Bunny


class Ai_player():

    def __init__(self):
        #inicialización de variables
        self.size_of_board = 10
        self.time_max_to_compute = 20
        self.valid_moves = []
        self.computing = False
        self.depth_of_game = 0
        self.aiba_player = 2
        self.ply_depth = 3
        self.board = Board.initialize_game_board(self.size_of_board)
        self.current_player = 1
        self.aiba_zone, self.human_zone =  Board.set_gamer_territory(self.board)
        self.moves_aiba=[]

        # Print initial program info
        print("Hoppers game with AI by María Inés Vásquez")
        print("Playing against: AI-ba")
        print()

    #función para calcular movimiento válidos
    def get_valid_moves(self, tile, calculated=None, adj=True, next_moves=False):

        #calcular pasos
        def step_moves(coord, delta_r, delta_c):
            return(coord.coord[0] + delta_r, coord.coord[1] + delta_c)  
        #calcular saltos
        def jump_moves(row, col, delta_r, delta_c):
            return(row+delta_r, col+delta_c)
        #regresar nueva posición
        def new_position(r, c):
            return self.board[r][c]

        #para adjuntar todos los movimientos se inicializa un arreglo
        if calculated is None:
            calculated = []

        # calcular todos los movimientos y solo regresar los validos
        for delta_c in range(-1, 2):
            for delta_r in range(-1, 2):

                #pasos
                step_r, step_c = step_moves(tile, delta_r, delta_c)
                #saltos
                jump_r, jump_c = jump_moves(step_r, step_c, delta_r, delta_c)

                #para revisar que me mantengo en el área del tablero o si el movimiento no es válido
                if ((step_r == tile.coord[0] and step_c == tile.coord[1]) or step_r < 0 or step_c < 0 or step_r >= self.size_of_board or step_c >= self.size_of_board or jump_r < 0 or jump_c < 0 or jump_r >= self.size_of_board or jump_c >= self.size_of_board):
                    continue

                # Mover pieza
                new_tile = new_position(step_r,step_c)
                
                if new_tile.piece == 0:
                    if adj:  # si ya se inicializo la busqueda, calcular saltos o pasos seguidos
                        calculated.append(new_tile)
                    continue

                # Mover pieza
                new_tile = new_position(jump_r,jump_c)
                #si ya fue calculado se excluye
                if new_tile in calculated: 
                    continue

                #si el espacio esta disponible, se agrega al arreglo y se sigue calculando hasta terminar todos los posibles
                if new_tile.piece == 0:
                    calculated.append(new_tile)
                    self.get_valid_moves(new_tile, calculated, False)

        return calculated

    #función para mover conejo
    def bunny_step(self, from_coord, to_coord):

    #cambio de paso o salto del conejo
        def new_location_bunny(from_coord, to_coord):
            # Mover pieza
            to_coord.piece = from_coord.piece
            from_coord.piece = 0
            self.depth_of_game += 1
        
        # Si la pieza no existe o donde desea moverlo está ocupado regresa mov no válido
        if from_coord.piece == 0 or to_coord.piece != 0:
            print("Movimiento inválido, vuelva a ingresar valores")
            return False
        #movimiento realizado
        new_location_bunny(from_coord, to_coord) 


#función para calcular ganador
    def win_analyzer(self):
        win_human=[]
        win_alba=[]
        # por cada pieza del área de AI-ba se verifica si todas están ocupadas por humano
        for g in self.aiba_zone:
            ind = (g.piece == 1)
            win_human.append(ind)
        
        #si todas dan verdadero gana humano
        if (all(win_human)==True):
            return 1
        
        # por cada pieza del área del humano se verifica si todas están ocupadas por AI-ba
        for g in self.human_zone:
            ind = (g.piece == 2)
            win_alba.append(ind)

        #si todas dan verdadero gana AI-ba
        if (all(win_alba)==True):
            return 2
        
        return None

    #logica del turno de AI-ba
    def AIba_turn(self):
        #función de minimax
        def minimax(depth_to_reach, player_turn, max_time, a=float("-inf"), b=float("inf"), maxing=True):

            def possible_moves(player=1):
                moves = []  #calculo de posibles movimientos del jugador en turno
                for col in range(self.size_of_board):
                    for row in range(self.size_of_board):
                        curr_tile = self.board[row][col]
                        if curr_tile.piece != player:
                            continue
                        move = {}
                        move["from"]= curr_tile
                        move["to"] = self.get_valid_moves(curr_tile)
                        moves.append(move)
                return moves

            def heuristic_function(player):

                def distance_to_goal(p0):
                    #funcion heuristica se basa en escoger la distancia que más avance hasta la esquina del jugador opuesto
                    if (player ==2):
                        p1 = (9,9)
                        return (math.sqrt((p1[0] - p0[0])**2 + (p1[1] - p0[1])**2))*-1
                    else:
                        p1 = (0,0)
                        return (math.sqrt((p1[0] - p0[0])**2 + (p1[1] - p0[1])**2))

                value = 0
                
                for col in range(self.size_of_board):
                    for row in range(self.size_of_board):

                        tile = self.board[row][col]

                        if tile.piece == 1:
                            distances = distance_to_goal(tile.coord)
                            value -= distances

                        elif tile.piece == 2:
                            distances = distance_to_goal(tile.coord)
                            value += distances
                return value

            # regresar mejor valor en el caso que se ha llegado hasta el fondo, se ha ganado o el tiempo de ejecución a superado al máximo
            if depth_to_reach == 0 or self.win_analyzer() or time.time() > max_time:
                return heuristic_function(player_turn), None

            best_move = None

            #calculo de los posibles movimientos del max y el min
            if maxing:
                best_val = float("-inf")
                moves = possible_moves(player_turn)
            else:
                best_val = float("inf")
                moves = possible_moves((2
                        if player_turn == 1 else 1))
            # por cada movida se calcula si el tiempo ha sido superado, si no se sigue evaluando
            """print("============movimiento de alba===========================")
            print(moves)
            self.moves_aiba=moves"""
            for move in moves:
                """print("============origen===================")
                print(move["from"].coord)
                #print(move["to"])
                print("============destino===================")"""
                for to in move["to"]:
                    #print(to.coord)
                    if time.time() > max_time:
                        return best_val, best_move

                    # Movimiento de pieza en el tablero
                    piece = move["from"].piece
                    move["from"].piece = 0
                    to.piece = piece

                    #se vuelve a llamar recurivamente, per turnarndo al not maxing para desarrollar todos los nodos hasta la profundidad programada
                    val, _  = minimax(depth_to_reach - 1,
                        player_turn, max_time, a, b, not maxing )

                    # Se regresa la posición dado que no se ha seleccionado aún
                    to.piece = 0
                    move["from"].piece = piece

                    #si estamos en maxing y se consiguio un mejor movimiento se guarda hasta terminar de recorrer todo
                    if maxing and val > best_val:
                        best_val = val
                        best_move = (move["from"].coord, to.coord)
                        a = max(a, val)

                    #si estamos en min y se consiguio un mejor movimiento se guarda hasta terminar de recorrer todo
                    if not maxing and val < best_val:
                        best_val = val
                        best_move = (move["from"].coord, to.coord)
                        b = min(b, val)
                    #funcion de alpha-beta prunning para recortar el árbol de decisión
                    if b <= a:
                        return best_val, best_move
            #luego de terminar de revisar todos los movimientos se regresa el mejor movimiento encontrado para el jugador
            return best_val, best_move

        
        # Inicio de turno de AI-ba
        current_turn = (self.depth_of_game // 2) + 1
        print("Turn de AI-ba")
        print("--------------------------")
        print("Calculando ...")
        self.computing = True
        max_time = time.time() + self.time_max_to_compute

        # Se realiza el minimax de sus movimientos
        start = time.time()
        _, move  = minimax(self.ply_depth,
            self.aiba_player, max_time)
        end = time.time()

        #movimiento seleccionado se ejecuta
        print("===========aiba move===========")
        move_from_aiba = self.board[move[0][0]][move[0][1]]
        #print(move_from_aiba)

        self.moves_aiba = self.get_valid_moves(move_from_aiba)
        move_from = self.board[move[0][0]][move[0][1]]
        move_to = self.board[move[1][0]][move[1][1]]
        #print(self.moves_aiba)
        for a in self.moves_aiba:
            print(a.coord)
            if (a.coord==move_to.coord):
                break
        print("AI-ba se ha movido de "+str(move[0])+" a "+str(move[1]))
        self.bunny_step(move_from, move_to)
        #se calcula ganador, si ganó AI-ba se termina el juego
        winner = self.win_analyzer()
        if winner:
            print("AI-BA HA GANADO!")
            self.current_player = None
        #si no ha ganado se cede el turno al jugador humano
        else: 
            self.current_player = (2
                if self.current_player == 1 else 1)

        self.computing = False
        print()

        #XML that will be returned
        root = minidom.Document()
  
        xml = root.createElement('move') 
        root.appendChild(xml)
        
        productChild = root.createElement('from')
        productChild.setAttribute('row', str(move[0][0]))
        productChild.setAttribute('col', str(move[0][1]))

        toChild = root.createElement('to')
        toChild.setAttribute('row', str(move[1][0]))
        toChild.setAttribute('col', str(move[1][1]))
        
        xml.appendChild(productChild)
        xml.appendChild(toChild)

        path = root.createElement('path')
        xml.appendChild(path)

        for a in self.moves_aiba:
            print(a.coord)
            pos1 = root.createElement('pos')
            pos1.setAttribute('row', str(a.coord[0]))
            pos1.setAttribute('col', str(a.coord[1]))
            path.appendChild(pos1)
            if (a.coord==move_to.coord):
                break
          
        xml_str = root.toprettyxml(indent ="\t") 

        print(xml_str)
        return xml_str
    
    #Jugada de humano
    def human_player_move(self):
        current_turn = (self.depth_of_game // 2) + 1
        validation = True
        print("¡Tu turno!")
        print("----------------------------------")

        #ingreso de datos para mover conejo/ficha

        move_from_row = int(input("Ingrese fila de la pieza a mover:"))
        move_from_col = int(input("Ingrese columna de la pieza a mover :"))

        move_to_row = int(input("Ingrese fila a donde desea moverla:"))
        move_to_col = int(input("Ingrese columna a donde desea moverla :"))
        
        #se obtiene la pieza del tablero que desea mover
        move_from = self.board[move_from_row][move_from_col]
        #se calcula los movimientos validos desde ese
        """print("==========move from human============")
        print(move_from)"""
        self.valid_moves = self.get_valid_moves(move_from)
        #se obtiene la pieza del tablero de a donde desea moverse
        move_to = self.board[move_to_row][move_to_col]
        print("Te has movido de ("+str(move_from_row)+","+str(move_from_col)+") a ("+str(move_to_row)+","+str(move_to_col)+")")
        #si la nueva pieza no esta entre los validos vuelve a repetirse el turno
        print("============================Camino de pasos===============================")
        for i in self.valid_moves:
            print(i.coord)
        if (move_to not in self.valid_moves):
            print(move_to)
            print("Ese movimiento no es válido")
            return
        else:
            #si es valido se mueve
            validation = self.bunny_step(move_from, move_to)

        winner = self.win_analyzer()
        #si regresa que humanos es ganador se para el juego
        if winner:
            print("LE HAS GANADO A AIBA!")
            self.current_player = None
        #si la validacion es false vuelve a repetirse su turno
        elif (validation==False):
            self.human_player_move()
        #si sigue jugando y la movida fue valida le ceda el turno a AI-ba
        elif self.aiba_player is not None:
            self.AIba_turn()
        else:  #control de jugador actual
            self.current_player = (2
                if self.current_player == 1 else 1)
        

        

            
    
