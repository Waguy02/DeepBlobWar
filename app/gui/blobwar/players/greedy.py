from app.environments.blobwar.core.strategies.greedy import Greedy

from app.gui.blobwar.players.player import Player


class GreedyPlayer(Player):
    def __init__(self,name="Greedy"):
        super().__init__(name)
        self.greedy_strategy=Greedy()


    def choose_action(self,env):
        return self.greedy_strategy.compute_next_move(env.core)
