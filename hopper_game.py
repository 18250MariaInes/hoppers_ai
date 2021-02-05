"""
María Inés Vásquez Figueroa
18250
AI-ba player for Hopper board game
Main
"""

from ai_player import Ai_player


hopper = Ai_player()
while hopper.win_analyzer() == None:
    for i in hopper.board:
        for j in i:
            print(j.piece, end=" ")
        print()
    print("------------------------------------")
    hopper.human_player_move()