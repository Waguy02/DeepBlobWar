from game_model.strategies.human import *
from game_model.strategies.greedy import *
from game_model.configuration import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game:Configuration=Configuration( Board())
    game.battle(FoolishGreedy(),Greedy())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
