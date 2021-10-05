import board_size

from gui.blobwar.gui import BlobwarGui
from utils.register import get_environment


def main():
    blobwar_gui = BlobwarGui()
    blobwar_gui.setup()


if __name__=="__main__":
    main()
