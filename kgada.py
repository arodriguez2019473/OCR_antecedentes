import random

player_move =['rock, paper, or scissors?']

#                 0     1           2
valid_moves = ["rock", "paper", "scissors"]

player_move = None

while not player_move in valid_moves:
    player_move = input('rock, paper, or scissors? \n')

    # rock

random_number = random.randrange(0,3)    
# 2
computer_move = valid_moves[random_number]

if player_move == computer_move:
    print("__________")
    print('tie!')
    print("=============")

elif player_move == 'rock' and computer_move == 'scissors': 
    print("__________")
    print('you win!')
    print("=============")


elif player_move == 'scissors' and computer_move == 'paper': 

    print("__________")
    print('you win!')
    print("=============")


elif player_move == 'paper' and computer_move == 'rock': 

    print("__________")
    print('you win!')
    print("==========")

else: print('\n computer wins better luck next time')
