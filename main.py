

from game_model.board import *
from game_model.human import *
from game_model.configuration import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game:Configuration=Configuration( Board(10,10))
    game.battle(Human(),Human())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
