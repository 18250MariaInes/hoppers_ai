from ai_player import Ai_player


hopper = Ai_player()
while hopper.find_winner() == None:
    for i in hopper.board:
        for j in i:
            print(j.piece, end=" ")
        print()
    print("------------------------------------")
    hopper.human_player_move()