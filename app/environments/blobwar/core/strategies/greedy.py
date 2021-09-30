

from environments.blobwar.core.strategies.strategy import*
import random

""":cvar
A greedy strategy for the game 
"""
class Greedy(Strategy):

    def __init__(self):
        pass


    def name(self):
        return "Greedy"


    def compute_next_move(self,configuration):
        moves=configuration.movements()

        if len(moves)>0:
            move_max=None
            value_max=-100000000000
            for move in moves:
                clone_conf=configuration.play(move)
                clone_conf.current_player*=-1;
                value=clone_conf.value()
                if value>value_max:
                    value_max=value
                    move_max=move


            return move_max


        else :
            return None


"""
This algo will choose random moves
"""
class FoolishGreedy(Strategy):
    def __init__(self):
        pass
    def name(self):
        return "Foolish Greedy"
    def compute_next_move(self,configuration):
        moves=configuration.movements()

        if len(moves)>0:
            return moves[int(random.random()*len(moves))] #Randomly choose un move


        else :
            return None

