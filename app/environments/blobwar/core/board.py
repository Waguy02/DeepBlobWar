
import numpy as np
from environments.blobwar.board_size import get_size

class Board:
    def __init__(self,xsize=None,ysize=None,initial_positions:[]=-1):


        if xsize is None or ysize is None:
            xsize=ysize=get_size()

        self.shape=(xsize,ysize)
        self.initial_positions=initial_positions
        self.initialize_positions()


    def initialize_positions(self):
        (xsize, ysize)=self.shape
        self.positions=np.zeros(self.shape)  # a 2ndarray, for each position : the value = 0 (empty) 1 => player1 and -1=>player2
        if self.initial_positions==-1:
            self.positions[0][0]=1
            self.positions[xsize-1][ysize-1]=1
            self.positions[0][ysize-1]=-1
            self.positions[xsize-1][0]=-1
        else:
            for xi,yi,pi in self.initial_positions:
                assert (xi<xsize)
                assert (yi<ysize)
                self.positions[xi][yi]=pi

    def clone(self):
        clone_board=Board(self.shape[0],self.shape[1],[])
        clone_board.positions=self.positions.copy()
        return clone_board

    def __getitem__(self, key):
        return self.positions[key]




