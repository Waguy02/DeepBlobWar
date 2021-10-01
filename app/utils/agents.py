import sys
import numpy as np

from environments.blobwar.constants import SIZE

np.set_printoptions(threshold=sys.maxsize)
import random
import string

import config

from stable_baselines import logger

def sample_action(action_probs):
    action = np.random.choice(len(action_probs), p = action_probs)
    return action


def mask_actions(legal_actions, action_probs):

    masked_action_probs = np.multiply(legal_actions, action_probs)
    masked_action_probs = masked_action_probs / np.sum(masked_action_probs)
    return masked_action_probs


class Agent():
  def __init__(self, name, model = None):
      self.name = name
      self.id = self.name + '_' + ''.join(random.choice(string.ascii_lowercase) for x in range(5))
      self.model = model
      self.points = 0

  def format_action(self, action):

      return action
      xsize = SIZE
      ysize = SIZE

      x1 = int(action / ((xsize) * (ysize ** 2)))
      action = action - ((xsize) * (ysize ** 2)) * x1

      y1 = int(action / (xsize * (ysize)))
      action = action - ((xsize) * (ysize)) * y1

      x2 = int(action / (xsize))
      action - ((xsize)) * x2
      y2 = action % xsize
      return [(x1, y1), (x2, y2)]


  def print_top_actions(self, action_probs):
    top5_action_idx = np.argsort(-action_probs)[:5]
    top5_actions = action_probs[top5_action_idx]
    formatter =self.format_action
    logger.debug(f"Top 5 actions: {[str(formatter(i)) + ': ' + str(round(a, 5)) for i, a in zip(top5_action_idx, top5_actions)]}")

  def choose_action(self, env, choose_best_action, mask_invalid_actions):
      if self.name=="greedy":
        return self.greedy(env, choose_best_action, mask_invalid_actions)


      if self.name == 'rules':
        action_probs = np.array(env.rules_move())
        value = None
      else:
        action_probs = self.model.action_probability(env.observation)
        value = self.model.policy_pi.value(np.array([env.observation]))[0]
        logger.debug(f'Value {value:.2f}')

      # logger.debug(f'\n action probs:{action_probs} ')
      self.print_top_actions(action_probs,env=env)

      if mask_invalid_actions:
        action_probs = mask_actions(env.legal_actions, action_probs)
        logger.debug('Masked ->')
        self.print_top_actions(action_probs)
        
      action = np.argmax(action_probs)

      formatter = self.format_action

      logger.debug(f'Best action {formatter(action)}')

      if not    choose_best_action:
          action = sample_action(action_probs)
          logger.debug(f'Sampled action {formatter(action)} chosen')

      return action



  def greedy(self, env, choose_best_action, mask_invalid_actions):
      max_action = None
      max_reward = -1

      legal_actions=env.legal_actions
      for action in range(len(legal_actions)):
          if legal_actions[action]==0:
              continue
          obs, rewards, done, _ = env.step(action,update=False)
          reward=rewards[env.current_player]
          if reward >max_reward:
              max_action=action
              max_reward=reward
              # logger.debug(f'Max reward: {max_reward}')

      return max_action







