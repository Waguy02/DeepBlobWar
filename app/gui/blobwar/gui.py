import time

from game2dboard import Board
from enum import Enum

from gym.envs import game

from gui.blobwar.players.greedy import GreedyPlayer
from gui.blobwar.players.human import Human
from gui.blobwar.players.ppo import PPO

from utils.register import get_environment


class GameState(Enum):
    WAITING_FIRST_CLICK = 0
    WAITING_SECOND_CLICK = 1
    GAME_OVER=2

class GameType(Enum):
    HUMAN_AI=0
    HUMAN_HUMAN=1
    AI_AI=2

PLAYER1_COLOR="blue"
PLAYER2_COLOR="orange"

class BlobwarGui:
    def __init__(self,simulation_mode=False):
        """:cvar
        """

        env = get_environment("blobwar")()
        env.seed(10)
        self.images={1:"blob_blue",2:"blob_orange"}
        self.images_selected= {1: "blob_blue_selected", 2: "blob_orange_selected"}
        self.images_candidates={1: "blob_blue_candidate", 2: "blob_orange_candidate"}
        self.env=env
        self.human_player=Human()
        try :

            self.ai_player_1 =PPO(self.env, size=self.env.core.board.shape[0])
        except Exception as e:
            print("PPO not yet trained for : ",self.env.core.board.shape[0])
            self.ai_player_1 = GreedyPlayer()

        self.ai_player_2 =GreedyPlayer()
        self.player1=self.player2=None

        if simulation_mode:
            self.state=GameState.WAITING_FIRST_CLICK
            self.player1 =self.ai_player_1
            self.player2 =self.player1
            return


        self.game=Board(self.env.core.board.shape[0],self.env.core.board.shape[1])

        self.game.cell_size = 70

        self.game.cell_spacing = 1
        self.game.fill(None)

        self.game.margin_color = self.game.grid_color = "wheat4"
        self.game.cell_color = "white"
        self.game.title = "Blobwar"
        self.game.create_output(font_size=11)
        self.state=GameState.GAME_OVER

        self.move_start_case=None
        self.move_candidates_case=[]






    def __player_num__(self, num):
        return min(2 - num, 2)  # 1=>1, -1 =>2

    def initialize(self,game_type=GameType.HUMAN_AI):
        """:cvar
        Initiliaze game and set automove if current player is not human
        """

        if game_type ==GameType.HUMAN_AI:
            self.player1=self.human_player
            self.player2=self.ai_player_1

        elif game_type==GameType.HUMAN_HUMAN:
            self.player1=self.human_player
            self.player2=self.human_player

        else:
            self.player1=self.ai_player_1
            self.player2=self.ai_player_2
        self.env.core.reset()
        self.state=GameState.WAITING_FIRST_CLICK

        self.move_start_case=None
        self.move_candidates_case=[]
        self.render()


        if not isinstance(self.player1,Human) and not isinstance(self.player2,Human):
            self.autoplay()
        else:
            self.state=GameState.WAITING_FIRST_CLICK
            self.print_status()
            if not isinstance(self.player1,Human):
                movement = self.player1.choose_action(self.env)
                self.env.core.apply_movement(movement)
                self.print_status()
                self.render()

    def render(self):
        for x in range(self.env.core.board.shape[0]):
            for y in range(self.env.core.board.shape[1]):
                if self.env.core.board[x][y]==0:
                    self.game[x][y]=None
                    continue
                self.game[x][y]=self.images[self.__player_num__(self.env.core.board[x][y])]

        if self.move_start_case is not None:
            self.render_selected()




    def fnkbd(self,key):
        if key == "Escape":
            self.game.close()
        elif key == "F2":
            self.initialize(game_type=GameType.HUMAN_AI)
        elif key == "F3":
            self.initialize(game_type=GameType.HUMAN_HUMAN)

        elif key == "F4":
            self.initialize(game_type=GameType.AI_AI)

    def setup(self):
        self.game.on_mouse_click = self.on_click
        self.game.on_key_press = self.fnkbd
        self.game.on_start =lambda: self.initialize()
        self.game.show()



    def on_click(self,btn,x,y):
        current_player=self.player1 if self.__player_num__(self.env.core.current_player) == 1 else self.player2

        if not isinstance(current_player, Human):
            return


        if self.state==GameState.GAME_OVER:
            return
        if self.state==GameState.WAITING_FIRST_CLICK:
            self.__on_first_click(btn,x,y)
            return

        if self.state==GameState.WAITING_SECOND_CLICK:
            self.__on_second_click(btn,x,y)
            return

    def __on_first_click(self,btn, x, y):
        if self.env.core.board[x][y]==0:
            return
        current_player=self.__player_num__(self.env.core.current_player)
        if self.__player_num__(self.env.core.board[x][y]) !=current_player:
            return

        else :
            self.move_start_case=(x, y)
            self.move_candidates_case=self.env.core.neighbours(x,y)
            self.render()
            self.state=GameState.WAITING_SECOND_CLICK

    def __on_second_click(self,btn,x,y):
        current_player = self.__player_num__(self.env.core.current_player)
        if (x,y)==self.move_start_case:
            self.move_start_case = None
            self.move_candidates_case=[]
            self.render()
            self.state=GameState.WAITING_FIRST_CLICK
            return
        movement=[self.move_start_case, (x, y)]

        if  self.env.core.check_move(movement):
            self.env.core.apply_movement(movement)
            self.print_status()
            (x_start,y_start)=self.move_start_case
            self.game[x_start][y_start] = self.images[current_player]
            self.move_start_case=None
            self.move_candidates_case=[]
            self.state = GameState.WAITING_FIRST_CLICK
            self.render()

            ###Automatic play

            def after_move():
                current_player = self.player1 if self.__player_num__(self.env.core.current_player) == 1 else self.player2

                if self.env.core.game_over():
                    self.state = GameState.GAME_OVER
                    winner_id = self.env.core.leading_player()

                    self.render()
                    self.print_status()
                    return


                self.print_status()
                if not isinstance(current_player ,Human):
                    movement = current_player.choose_action(self.env)
                    # self.pause(1000)
                    self.env.core.apply_movement(movement)
                    self.print_status()

                else :
                    if len(self.env.core.movements())==0:
                        self.env.core.apply_movement(None)
                        self.print_status()

            after_move()
            self.render()

        else :
            x_old,y_old=self.move_start_case
            self.game[x_old][y_old] = self.images[current_player]
            self.move_candidates_case=[]
            if self.game[x][y]==self.images[current_player]:
                self.move_start_case=x,y
                self.move_candidates_case=self.env.core.neighbours(x,y)
                self.state=GameState.WAITING_SECOND_CLICK
            else:
                self.move_start_case = None
                self.move_candidates_case= []
                self.state=GameState.WAITING_FIRST_CLICK
            self.render()

            return


        if self.env.core.game_over():
            self.state=GameState.GAME_OVER
            self.print_status()

    def render_selected(self):
        if self.move_start_case is None:
            return
        current_player_num =self.__player_num__(self.env.core.current_player)
        x,y=self.move_start_case
        self.game[x][y] = self.images_selected[current_player_num]
        for (x_cand,y_cand) in self.move_candidates_case:
            self.game[x_cand][y_cand]=self.images_candidates[current_player_num]



    def autoplay(self):
        """:cvar
        Game Autoplay between two IA players
        """
        while self.state!=GameState.GAME_OVER :
            current_player = self.player1 if self.__player_num__(self.env.core.current_player) == 1 else self.player2
            movement = current_player.choose_action(self.env)
            self.env.core.apply_movement(movement)
            if self.env.core.game_over():
                self.state=GameState.GAME_OVER
            self.print_status()
            self.pause(50)
            self.render()


    def simulate(self):
        """:cvar
        Game Autoplay between two IA players
        """
        while self.state!=GameState.GAME_OVER :
            current_player = self.player1
            movement = current_player.choose_action(self.env)
            self.env.core.apply_movement(movement)
            if self.env.core.game_over():
                self.state=GameState.GAME_OVER

        self.env.core.reset()




    def print_status(self):
        current_player,current_player_color = (self.player1,PLAYER1_COLOR) if self.__player_num__(self.env.core.current_player) == 1 else (self.player2,PLAYER2_COLOR)


        player0_value=int(self.env.core.player_value(1))
        # scores=f" {self.player1.name}({PLAYER1_COLOR}) : {player0_value} ,  {self.player2.name}({PLAYER2_COLOR}) : {-1*player0_value}"

        header=f"\t{self.player1.name}({PLAYER1_COLOR}): {player0_value}   VS  {self.player2.name}({PLAYER2_COLOR}): {-player0_value}"
        restart_message="\n \tF2:Human vs AI   F3:Human vs Human   F4:AI vs AI "
        if self.env.core.game_over():
            winner_id = self.env.core.leading_player()
            winner = self.__player_num__(winner_id)
            winner_player = self.player1 if winner == 1 else self.player2
            winner_color=PLAYER1_COLOR if winner==1 else PLAYER2_COLOR

            if player0_value==0:
                current_message=f"\tDraw"
            else:
                current_message=f"\t{winner_player.name}({winner_color}) won!!"

        else:

            current_message=f"\t{current_player.name}({current_player_color})  playing ..."


        text=header+"\n"+current_message+"\n"+restart_message
        self.game.print(text)


    def pause(self,millis):

        self.game.pause(millis)

