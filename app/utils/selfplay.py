import os
import numpy as np
import random

from utils.files import load_model, load_all_models, get_best_model_name
from utils.agents import Agent


import config

from stable_baselines import logger

def selfplay_wrapper(env):

    class SelfPlayEnvBlobwar(env):
        """:
        Special SelfPlay For blobwar game. Some modifications. overriding of continue game and step methods to handle partial rewards.
        """
        # wrapper over the normal single player env, but loads the best self play model
        # wrapper over the normal single player env, but loads the best self play model
        def __init__(self, opponent_type, verbose):
            super(SelfPlayEnvBlobwar, self).__init__(verbose)
            self.opponent_type = opponent_type
            self.opponent_models = load_all_models(self)
            self.best_model_name = get_best_model_name(self.name)

        def setup_opponents(self):
            if self.opponent_type == 'rules':
                self.opponent_agent = Agent('greedy')
            else:
                # incremental load of new model
                best_model_name = get_best_model_name(self.name)
                if self.best_model_name != best_model_name:
                    self.opponent_models.append(load_model(self, best_model_name))
                    self.best_model_name = best_model_name

                if self.opponent_type == 'random':
                    start = 0
                    end = len(self.opponent_models) - 1
                    i = random.randint(start, end)
                    self.opponent_agent = Agent('ppo_opponent', self.opponent_models[i])

                elif self.opponent_type == 'best':
                    self.opponent_agent = Agent('ppo_opponent', self.opponent_models[-1])

                elif self.opponent_type == 'mostly_best':
                    j = random.uniform(0, 1)
                    if j < 0.8:
                        self.opponent_agent = Agent('ppo_opponent', self.opponent_models[-1])
                    else:
                        start = 0
                        end = len(self.opponent_models) - 1
                        i = random.randint(start, end)
                        self.opponent_agent = Agent('ppo_opponent', self.opponent_models[i])

                elif self.opponent_type == 'base':
                    self.opponent_agent = Agent('base', self.opponent_models[0])

            self.agent_player_num = np.random.choice(self.n_players)
            self.agents = [self.opponent_agent] * self.n_players
            self.agents[self.agent_player_num] = None
            try:
                # if self.players is defined on the base environment
                logger.debug(f'Agent plays as Player {self.players[self.agent_player_num].id}')
            except:
                pass

        def reset(self):
            super(SelfPlayEnvBlobwar, self).reset()
            self.setup_opponents()

            if self.current_player_num != self.agent_player_num:
                self.continue_game()

            return self.observation

        @property
        def current_agent(self):
            return self.agents[self.current_player_num]

        def continue_game(self):
            """Working with partial rewards and at the end of the round, sum up reward amount step"""
            adversary_round_rewards=[0,0]
            if self.current_player_num != self.agent_player_num:
                self.render()
                action = self.current_agent.choose_action(self, choose_best_action = False, mask_invalid_actions = False)
                #
                # if self.opponent_type == 'rules':
                #     assert(self.core.check_move(self.decode_action(action)),"Adversary rules based cannot play bad moves")

                observation, rewards, done, _ = super(SelfPlayEnvBlobwar, self).step(action)
                # formatted_action = super(SelfPlayEnvBlobwar, self).decode_action(action)
                logger.debug(f'Action played by adversary({"o" if self.agent_player_num==0 else "x"}): {action}')
                for i in range(len(self.agents)):
                    adversary_round_rewards[i]=rewards[i]
            return observation,  adversary_round_rewards, done, None

        def step(self, action):
            observation, agent_round_rewards, done, _ = super(SelfPlayEnvBlobwar, self).step(action)
            formatted_agent_action=super(SelfPlayEnvBlobwar, self).decode_action(action)
            logger.debug(f'Action played by agent({"x" if self.agent_player_num==0 else "0"}): {formatted_agent_action}')
            if not done:
                adversary_return = self.continue_game()
                if adversary_return is not None:
                    observation, adversary_round_rewards, done, _ = adversary_return
                total_rewards=[r_agent_round+r_adversary_round for (r_agent_round,r_adversary_round) in zip(agent_round_rewards,adversary_round_rewards)]
                logger.debug(f'Agent round Rewards: {agent_round_rewards}')
                logger.debug(f'Adversary round rewards: {adversary_round_rewards}')
                logger.debug(f'Total_round_reward: {total_rewards}')
                logger.debug(f'Done: {done}')
            else:
                total_rewards=agent_round_rewards
                logger.debug(f'Done: {done}')
                logger.debug(f'Total_round_reward: {total_rewards}')
            agent_reward = total_rewards[self.agent_player_num]
            logger.debug(f'Reward To Agent: {agent_reward}')
            self.render()
            return observation, agent_reward, done, {}



    return SelfPlayEnvBlobwar