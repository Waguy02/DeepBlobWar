from app.gui.blobwar.players.greedy import GreedyPlayer
from app.gui.blobwar.players.human import Human
from app.gui.blobwar.players.ppo import PPO
from app.gui.blobwar.gui import BlobwarGui
from app.utils.register import get_environment

if __name__=="__main__":
    env = get_environment("blobwar")()
    env.seed(10)
    blobwar_gui=BlobwarGui(env)
    blobwar_gui.setup()
