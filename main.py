from app.environments.blob_war.blob_core.strategies.human import *
from app.environments.blob_war.blob_core.strategies.greedy import *
from app.environments.blob_war.blob_core.configuration import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game:Configuration=Configuration( Board())
    game.battle(FoolishGreedy(),Greedy())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
