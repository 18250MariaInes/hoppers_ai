"""
María Inés Vásquez Figueroa
18250
AI-ba player for Hopper board game
Main
"""

from ai_player import Ai_player


hopper = Ai_player()

print("¡Bienvenid@ a jugar con AiBA!")
print("Seleccione el mode en el que quiere jugar:")
print("1) Humano vs AiBA")
print("2) AiBA vs AiBA")
modo = int(input("-->"))
if (modo==2):
    while hopper.win_analyzer() == None:
        for i in hopper.board:
            for j in i:
                print(j.piece, end=" ")
            print()
        print("------------------------------------")
        hopper.AIba_turn(1)
        for i in hopper.board:
            for j in i:
                print(j.piece, end=" ")
            print()
        print("------------------------------------")
        hopper.AIba_turn(2)
        
else:
    while hopper.win_analyzer() == None:
        for i in hopper.board:
            for j in i:
                print(j.piece, end=" ")
            print()
        print("------------------------------------")
        hopper.human_player_move() 
    