import numpy as np

from environments.blobwar.core.board import Board
from environments.blobwar.core.strategies.strategy import  Strategy
class Configuration:
    def __init__(self,board:Board):
        """
        :param board:
        :type board:
        :param initial_positions: A vector as a vec of [xi,yi,pi]

        """
        self.board=board
        self.current_player=1
        self.player1_name=""
        self.player2_name= ""

    def battle(self,player1:Strategy,player2:Strategy):
        self.player1_name=player1.name()
        self.player2_name = player2.name()
        while not self.game_over():
            self.display()
            if (self.current_player==1):
                attempt=player1.compute_next_move(self)
            else :
                attempt=player2.compute_next_move(self)

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
        print(self.toString())

    def toString(self,player1ID="player1",player2ID="player"):
        space_two = "   "
        space_one = " "
        output = "\n"+space_two + space_one
        for iy in range(self.board.shape[1]):
            output += str(iy) + space_one

        output += "\n"

        output += space_one+space_one+ "+" + space_one

        for iy in range(self.board.shape[1]):
            output += "-" + space_one

        output += "+\n"

        for ix in range(self.board.shape[0]):

            output += str(ix) + space_one + "|" + space_one

            for iy in range(self.board.shape[1]):
                val = self.board.positions[ix][iy]

                if val == -1:
                    output += "0" + space_one


                elif val == 0:
                    output += space_one + space_one

                elif val == 1:
                    output += "x" + space_one
            output += "|\n"
        output += space_one + space_one + "+" + space_one

        for iy in range(self.board.shape[1]):
            output += "-" + space_one

        output += "+\n"

        output += ""

        if self.current_player==1:
            id=1
            id_adverse=2
            active_name,adverse_name=self.player1_name,self.player2_name
            active_icon,adverse_icon="x","0"

        else:
            id=2
            id_adverse=1
            active_name = self.player2_name
            adverse_name = self.player1_name
            active_icon, adverse_icon = "0", "x"


        output += "Player" + str(id) +"("+active_icon+")"+ ":"+active_name + ":"+str(self.value()) + "  (Current player)\n"
        output += "Player" + str(id_adverse) +"("+adverse_icon+")"+ ":"+adverse_name + ":"+ str(self.adverse_value()) + "\n"

        return output


    def player_value(self,id):
        return self.board.positions.flatten().sum() * id

    def value(self):
        return self.player_value(self.current_player)

    def adverse_value(self):
        return -1*self.value()



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
        ## A duplication move is tuple ([xi,yi], [xf,yf])
        duplics = []

        ix_max, iy_max = self.board.shape[0], self.board.shape[1]
        for ix in range(ix_max):
            for iy in range(iy_max):
                if self.board.positions[ix][iy] != self.current_player:
                    continue
                for neighbour in self.__neighbours__(ix, iy,distance=1):
                    duplics.append([(ix, iy), neighbour])
        return duplics

    def bad_moves(self):
        bad_moves=[]
        for xi in range(self.board.shape[0]):
             for yi in range(self.board.shape[1]):
                 for xf in range(self.board.shape[0]):
                    for yf in range(self.board.shape[1]):
                        mvt=[(xi,yi),(xf,yf)]

                        if self.board.positions[xi][yi]!=self.current_player:
                            bad_moves.append(mvt)
                            continue
                        if not self.check_move(mvt):
                            bad_moves.append(mvt)
        return bad_moves

    def check_move(self,mvt:[])->bool:
        if mvt==None: ##Can perform empty move
            return True
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

    def total_movements(self):
        return self.movements()+self.bad_moves()

    def move_to_nd_array(self,move):
        return np.array([[move[0][0],move[0][1]],[move[1][0],move[1][1]]])

    def total_movements_nd_array(self):
        return [self.move_to_nd_array(move) for move in self.total_movements()]


    def apply_movement(self, mvt: []):
        if mvt is not None:
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

        if np.abs(flatten_positions.sum())==non_zeros: ##Only one remaining player
            return True

        return False

    def leading_player(self):
        value1=self.value()
        self.current_player*=-1
        value2=self.value()

        self.current_player *= -1

        if value1>value2:
            return self.current_player
        if value1<value2:
            return -1*self.current_player
        return 0


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
        :return: The tuple of free neighbours
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
    Check if a move is a jump
    """
    def __is_jump__(self, mvt):
        return self.distance(mvt)==2
    































