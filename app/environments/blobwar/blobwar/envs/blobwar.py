# Adapted from https://mblogscode.com/2016/06/03/python-naughts-crossestic-tac-toe-coding-unbeatable-ai/

import gym
import numpy as np
from app.environments.blobwar.core.board import Board
from app.environments.blobwar.core.configuration import Configuration


import config

# from stable_baselines import logger
import logger

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
        self.core=Configuration(Board())

        xsize=self.core.board.shape[0]
        ysize=self.core.board.shape[1]
        nb_cells = self.core.board.shape[0] * self.core.board.shape[1]
        self.observation_space = gym.spaces.Box(-1, 1, self.core.board.shape,dtype=int)  # board 8x8
        ## Actions: No of players (2) ** Nb of cases
        ### Encode actions as integers
        self.action_space =gym.spaces.Discrete(xsize*xsize*ysize*ysize)

    @property
    def observation(self):
        return self.core.board.positions


    @property
    def legal_actions(self):
        legal_actions=[1 if self.core.check_move(self.map_action(action)) else -1 for action in range(self.action_space.n)]
        return np.array(legal_actions)




    ###Check if the game is over
    def check_game_over(self):

        is_over=self.core.game_over()
        if is_over:
            if self.core.leading_player()==self.core.current_player:
                return 1,True ## If the current player is winnig
            else:
                return 0,True ## otherwise


        return 0,False

    """
    map an actoin from integer { 0,1..., xsize*ysize} to [[8,8] [8,8]]
    
    """
    def map_action(self, action):
        xsize=self.core.board.shape[0]
        ysize=self.core.board.shape[1]

        x1=int(action/((xsize)*(ysize**2)))
        action=action-((xsize)*(ysize**2))*x1

        y1= int(action/(xsize*(ysize)))
        action = action - ((xsize) * (ysize)) * y1

        x2=int(action/(xsize))
        action - ((xsize)) * x2

        y2=action%xsize
        return [(x1,y1 ),(x2, y2)]



    @property
    def current_player(self):
        return min(2 - self.core.current_player, 2) -1   #1=>0, -1 =>1

    def step(self, action):
        move=self.map_action(action)

        old_values=[self.core.adverse_value(),self.core.value()]

        if not self.core.check_move(move):
            done=True
            move=None
            self.core.apply_movement(move)
            new_values=[old_values[0]-1000,old_values[1]] ## Highly penalise bad moves

        else :
            r, done = self.check_game_over()
            self.core.apply_movement(move)
            ## The player become the adversary
            new_values=[self.core.adverse_value(),self.core.value()]

        rewards=[new_values[0]-old_values[0],new_values[1]-old_values[1]]
        if self.core.current_player==-1: ##Reverse array of rewards
            rewards.reverse()

        return self.core.board.positions, rewards , done, {}

    def reset(self):
        self.board = [Token('.', 0)] * self.num_squares
        self.players = [Player('1', Token('X', 1)), Player('2', Token('O', -1))]
        self.core=Configuration(Board())

        return self.observation

    def render(self, mode='human', close=False, verbose=True):
        logger.debug(self.core.toString())









