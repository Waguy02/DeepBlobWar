import board_size

from gui.blobwar.gui import BlobwarGui
from utils.register import get_environment
from timeit import default_timer as timer

from tqdm import tqdm
import timeit

NB_SIMULATIONS=10000000
def main():
    blobwar_gui = BlobwarGui(simulation_mode=True)
    start = timer()
    for _ in tqdm(range(NB_SIMULATIONS)):
        blobwar_gui.simulate()
    end = timer()

    print(end - start)

if __name__=="__main__":
    main()
