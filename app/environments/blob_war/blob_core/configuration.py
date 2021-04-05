import numpy as np
from app.environments.blob_war.blob_core.board import  Board
from app.environments.blob_war.blob_core.strategies.strategy import  Strategy
from app.environments.blob_war.blob_core.strategies.greedy import Greedy
class Configuration:
    def __init__(self,board:Board):
        """
        :param board:
        :type board:
        :param initial_positions: A vector as a vec of [xi,yi,pi]

        """
        self.board=board
        self.current_player=1


    def battle(self,player1:Strategy,player2:Strategy):
        while not self.game_over():
            playerId=min(2-self.current_player,2) # 1= > player1; -1=> player2
            (icon,playerName)=("x",player1.name()) if playerId==1 else ("O",player2.name())

            self.display()
            print("Player"+str(playerId)+":"+playerName+ "("+icon+") is playing... His score is actually : ", self.value(), "\n")

            attempt=None
            if (self.current_player==1):
                attempt=player1.compute_next_nove(self)
            else :
                attempt=player2.compute_next_nove(self)


            if  attempt!=None:
                assert(self.check_move(attempt))
                self.apply_movement(attempt)
            else :
                self.current_player*=-1


        self.current_player=1
        value1=self.value()

        self.current_player=-1
        value2=self.value()

        self.display()
        if value1>value2:
            print("Player 1 :"+playerName+"  won, score : ",value1)
            return 1
        if value1==value2:
            print("Draw  , score : ", value1)
            return 0
        else:
            print("Player 2:"+playerName+" won, score : ",value2)
            return -1






    def display(self):
        space_two="   "
        space_one=" "

        print(space_two,end=space_one)
        for iy in range(self.board.shape[1]):
            print(iy,end=space_one)
        print(space_two)

        print(space_one,"+",end=space_one)
        for iy in range(self.board.shape[1]):
            print("-",end=space_one)
        print("+")

        for ix in range(self.board.shape[0]):
            print(ix,"|",end=space_one)

            for iy in range(self.board.shape[1]):
                val=self.board.positions[ix][iy]

                if val==-1:
                    print("0",end=space_one)

                elif val==0:
                    print(space_one,end=space_one)

                elif val==1:
                    print("x",end=space_one)
            print("|")

        print(space_one,"+", end=space_one)
        for iy in range(self.board.shape[1]):
            print("-", end=space_one)
        print("+")

    def value(self):
        return self.board.positions.flatten().sum()*self.current_player

    def jumps(self)->[]:
        ## A jump is tuple ([xi,yi], [xf,yf])
        jumps=[]

        ix_max,iy_max=self.board.shape[0],self.board.shape[1]
        for ix in range(ix_max):
            for iy in range(iy_max):
                if self.board.positions[ix][iy] != self.current_player:
                    continue
                for neighbour in self.__neighbours__(ix, iy, distance=2):
                    jumps.append([(ix,iy),neighbour])
        return jumps

    def duplicates(self)->[]:
        ## A jump is tuple ([xi,yi], [xf,yf])
        duplics = []

        ix_max, iy_max = self.board.shape[0], self.board.shape[1]
        for ix in range(ix_max):
            for iy in range(iy_max):
                if self.board.positions[ix][iy] != self.current_player:
                    continue
                for neighbour in self.__neighbours__(ix, iy,distance=1):
                    duplics.append([(ix, iy), neighbour])
        return duplics


    def check_move(self,mvt:[])->bool:

        def check_in_board(x,y):
            return x>=0 and x<self.board.shape[0] and y>=0 and y<self.board.shape[1]


        x_source, y_source = mvt[0]
        x_dest, y_dest = mvt[1]

        if not check_in_board(x_source,y_source) or not check_in_board(x_dest,y_dest):
            return False

        if self.distance(mvt)!=1 and self.distance(mvt)!=2:
            return False


        if self.board.positions[x_source][y_source]!=self.current_player:
            return False

        if not self.__is_free__(x_dest,y_dest):
            return False

        return True


    def movements(self)->[]:
        return self.duplicates()+self.jumps()

    def apply_movement(self, mvt: []):
        x_source, y_source = mvt[0]
        x_dest, y_dest = mvt[1]

        self.board.positions[x_dest][y_dest] = self.current_player
        if self.__is_jump__(mvt):
            self.board.positions[x_source][y_source] = 0  ## Free the source case when performing a jump

        for (x_adv, y_adv) in self.__adverse_neighbours__(x_dest, y_dest):
            self.board.positions[x_adv][y_adv] = self.current_player

        self.current_player = -1 * self.current_player

    def play(self, mvt: []):
        clone_conf = self.clone()
        clone_conf.apply_movement(mvt)
        return clone_conf

    def skip_play(self, mvt: []):
        clone_conf = self.clone()
        clone_conf.current_player = -1 * clone_conf.current_player
        return clone_conf

    def clone(self):
        clone_conf = Configuration(self.board.clone())
        clone_conf.current_player=self.current_player
        return clone_conf

    def distance(self, mvt: []):
        source = mvt[0]
        destination = mvt[1]

        return max(np.abs(source[0] - destination[0]), np.abs(source[1] - destination[1]))

    def game_over(self):
        flatten_positions=self.board.positions.flatten()
        non_zeros=np.count_nonzero(flatten_positions)
        if non_zeros==len(flatten_positions):## ALl cases taken
            return True

        sum=flatten_positions.sum() ## Only  one player remainnng
        if np.abs(sum)==non_zeros:
            return True


        return False














    def __is_free__(self, ix, iy)->bool:
        return self.board.positions[ix][iy]==0

    def __is_adverse__(self, ix, iy)->bool:
        return self.board.positions[ix][iy]==-1*self.current_player

    def __neighbours__(self, ix, iy, distance=None)->[]:
        """
        :param ix:
        :type ix:
        :param iy:
        :type iy:
        :return: The tupe of free neighbours
        :rtype:
        """
        ix_max, iy_max = self.board.shape[0], self.board.shape[1]
        neighbours=[]

        if distance==None:
            return self.__neighbours__(ix, iy, distance=1) + self.__neighbours__(ix, ix, distance=2) #Combine all neighbours
        
        

        for dx in [-distance,0, distance]:
            for dy in [-distance,0,distance]:
                if ix+dx<0 or ix+dx>=ix_max or iy+dy<0 or iy+dy>=iy_max:
                    continue
                if self.__is_free__(ix + dx, iy + dy):
                    neighbours.append((ix+dx,iy+dy))

        return neighbours
    
    
    def __adverse_neighbours__(self, ix, iy)->[]:
        ix_max, iy_max = self.board.shape[0], self.board.shape[1]
        neighbours = []

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if ix + dx < 0 or ix + dx >= ix_max or iy + dy < 0 or iy + dy >= iy_max:
                    continue
                if self.__is_adverse__(ix + dx, iy + dy):
                    neighbours.append((ix + dx, iy + dy))

        return neighbours

            
    """
    ¨Play mvt according to a given configuration
    """
    def __is_jump__(self, mvt):
        return self.distance(mvt)==2
    































