from  environments.blobwar.blobwar.envs.blobwar import BlobWarEnv
from  environments.blobwar.core.board import Board
from  environments.blobwar.core.strategies.human import *
from  environments.blobwar.core.strategies.greedy import *
from  environments.blobwar.core.configuration import *
# from  environments.blobwar.blobwar.envs.blobwar import  *
# Press the green button in the gutter to run the script.

def test_spaces():
    env=BlobWarEnv()


if __name__ == '__main__':
    test_spaces()
    game:Configuration=Configuration( Board())
    # print(len(game.movements().n))
    #

    game.battle(Human(),Greedy())

