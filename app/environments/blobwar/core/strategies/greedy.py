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
            moves_tuple=[(move,configuration.play(move).value()) for move in moves]
            moves_sorted=sorted(moves_tuple,key=lambda item: item[1])
            moves_max=[moves_sorted[0]]
            for k,v in moves_tuple[1:]:
                if v==moves_max[0][1]:
                    moves_max.append((k,v))
            best_move=random.choice(moves_max)[0]
            return best_move
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

