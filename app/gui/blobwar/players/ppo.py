from app.gui.blobwar.players.player import Player
from utils.files import load_model, write_results
from utils.agents import Agent

class PPO(Player):
    def __init__(self,env,name="AI_PPO",size=6):
        super().__init__(name)
        # make environment
        ppo_model=load_model(env, f'best_model{size}.zip')
        self.ppo_agent = Agent('best_model', ppo_model)

    def choose_action(self,env):
        action =self.ppo_agent.choose_action(env, choose_best_action=False, mask_invalid_actions=True)
        return env.decode_action(action)
