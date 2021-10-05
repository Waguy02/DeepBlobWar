from app.gui.blobwar.players.player import Player

class Human(Player):
    def __init__(self,name="Human"):
        super().__init__(name)
    def choose_action(self,env):
        pass