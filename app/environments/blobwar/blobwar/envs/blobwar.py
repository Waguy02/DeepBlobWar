# Adapted from https://mblogscode.com/2016/06/03/python-naughts-crossestic-tac-toe-coding-unbeatable-ai/

import gym
import numpy as np
from environments.blobwar.core.board import Board
from environments.blobwar.board_size import get_size
from environments.blobwar.core.configuration import Configuration

from stable_baselines import logger
class Player():
    def __init__(self, id, token):
        self.id = id
        self.token = token
class Token():
    def __init__(self, symbol, number):
        self.number = number
        self.symbol = symbol
class BlobWarEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    def __init__(self, verbose=False, manual=False):
        super(BlobWarEnv, self).__init__()
        self.name = 'blobwar'
        self.manual = manual

        size=get_size()
        self.core=Configuration(Board(xsize=size,ysize=size))
        self.n_players=2
        self.current_player_num=0
        self.xsize=self.core.board.shape[0]
        self.ysize=self.core.board.shape[1]

        self.observation_space = gym.spaces.Box(-1, 1, (self.xsize +self.xsize**2*self.ysize,self.ysize)+(1,)) # board 8x8[3 type of positions) #Pass legal actions to observation vector
        self.action_space =gym.spaces.Discrete((self.xsize**2)*(self.ysize**2))### Encode actions as integers ,the last action correspond to None move
        self.verbose=verbose
    @property
    def observation(self):
        positions_grid= self.core.board.positions.reshape((self.xsize,self.ysize,1))
        legal_actions_grid=np.reshape(self.legal_actions,(self.xsize**2*self.ysize,self.ysize,1))
        out = np.concatenate([positions_grid,legal_actions_grid])
        return out

    @property
    def legal_actions(self):
        legal_actions={self.encode_action(move) for move in self.core.movements()}
        legal_actions=[1 if action in legal_actions else 0 for action in range(self.action_space.n)]
        if np.sum(legal_actions)>1:
            legal_actions[self.encode_action(None)]=0 ##None action is only legal when it is the only possible action

        return np.array(legal_actions)
    ###Check if the game is over
    def check_game_over(self):

        is_over=self.core.game_over()
        if is_over:
            if self.core.leading_player()!=self.core.current_player:
                return 1,True ## If the current player is winnig
            else:
                return 0,True ## otherwise


        return 0,False
    """
    decode an action from integer { 0,1..., xsize*ysize} to [[8,8] [8,8]]
    """
    def decode_action(self, action):
        """
        Decode an integer encoded action as a move from a position to another
        :param action:
        :type action:
        :return:
        :rtype:
        """
        if action is None:
            return None

        xsize=self.core.board.shape[0]
        ysize=self.core.board.shape[1]

        x1=int(action/((xsize)*(ysize**2)))
        action=action-((xsize)*(ysize**2))*x1

        y1= int(action/(xsize*(ysize)))
        action = action - ((xsize) * (ysize)) * y1

        x2=int(action/(xsize))
        action - ((xsize)) * x2

        y2=action%xsize

        if x1==0 and x2==xsize-1 and y1==0 and y2==ysize-1:
            #Consider this particular action as none action (Condition x_size and y _size >3)
            return None

        return [(x1,y1 ),(x2, y2)]

    def encode_action(self,move):
        if move==None:
            return self.encode_action([(0,0),(self.xsize-1,self.ysize-1)])
        x1,y1=move[0]
        x2,y2=move[1]
        xsize=self.xsize
        ysize=self.ysize
        return y2+x2*xsize+y1*xsize*ysize +x1*(xsize**2)*ysize


    @property
    def current_player(self):
        return min(2 - self.core.current_player, 2)-1   #1=>0, -1 =>1

    def step(self, action,update=True):
        move=self.decode_action(action)
        old_value=self.core.value()
        player_num=self.current_player ##The player num before move beginning
        if not self.core.check_move(move):
            done=True ##End game on bad move
            move=None
            if update:
                self.core.apply_movement(move)
            r=-self.xsize*self.ysize
            rewards=[-r,r]
            rewards[player_num]=-1 ##Penalize bad moves
        else :
            self.core.apply_movement(move)
            new_value = self.core.adverse_value()
            r, done = self.check_game_over()
            reward=new_value-old_value if not done else new_value
            rewards=[-reward,-reward]
            rewards[player_num]=-1*rewards[player_num]

        self.current_player_num=self.current_player
        return self.observation, rewards , done, {}

    def reset(self):
       self.core=Configuration(Board())
       self.current_player_num=self.current_player
       obs=self.observation
       self.done=False
       return obs

    def render(self, mode='human', close=False, verbose=True):
        logger.debug(self.core.toString())
        # logger.debug(f'\nLegal actions: {[str(i) +":" + str(self.decode_action(i)) for i, o in enumerate(self.legal_actions) if o != 0]}')









