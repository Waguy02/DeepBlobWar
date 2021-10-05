import sys
import numpy as np
from environments.blobwar.core.strategies.greedy import Greedy



np.set_printoptions(threshold=sys.maxsize)
import random
import string


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

      self.greedies_strategies={"blobwar":Greedy()}






  def print_top_actions(self, action_probs,env=None):
    top5_action_idx = np.argsort(-action_probs)[:5]
    top5_actions = action_probs[top5_action_idx]

    if env is not None and env.name=="blobwar":
        formatter =env.decode_action
    else :
        formatter=lambda  action:action

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
        self.print_top_actions(action_probs,env=env)
        
      action = np.argmax(action_probs)

      formatter = env.decode_action  if env is not None and env.name=="blobwar" else lambda action:action

      logger.debug(f'Best action {formatter(action)}')

      if not    choose_best_action:
          action = sample_action(action_probs)
          logger.debug(f'Sampled action : {formatter(action)} chosen')

      return action



  def greedy(self, env, choose_best_action, mask_invalid_actions):
      if env.name=="blobwar":
          greedy=self.greedies_strategies["blobwar"]
          max_action=env.encode_action(greedy.compute_next_move(env.core))
          return max_action

      else:
          raise Exception("Greedy Strategy not implemented for game  "+env.name)







