from nes_py.wrappers import JoypadSpace
import os
import pickle

from learning.q_learning import QLearningAgent
from src.mario_agent import CustomMarioAgent
from src.mario_view import CustomMarioView
from src.mario_env import CustomMarioEnv
from utils.actions import (
    rom,
    actions,
)

def main():
    bdi_agent = CustomMarioAgent(actions)
    rl_agent = QLearningAgent(actions=["noop", "jump", "move_right"])
    view = CustomMarioView()
    env = JoypadSpace(CustomMarioEnv(rom), actions)
    
    obs = env.reset()
    done = False
    
    bdi_agent.update_beliefs(obs, info={})
    state = bdi_agent.beliefs

    q_table_path = "q_table.pkl"
    if os.path.exists(q_table_path):
        with open(q_table_path, "rb") as f:
            rl_agent.q_table = pickle.load(f)
        print("[INFO] Q-table carregada.")
    else:
        print("[INFO] Iniciando nova Q-table.")

    for step in range(10000):
        if done:
            obs = env.reset()
            bdi_agent.update_beliefs(obs, info={})
            state = bdi_agent.beliefs
            continue

        if view.is_start_screen(obs):
            env.step(7)
            continue

        intention = rl_agent.choose_action(state)
        action_map = {
            "noop": 0,         # ['NOOP']
            "move_right": 1,   # ['right']
            "jump": 5          # ['A']
        }
        action = action_map.get(intention, 0)


        obs, reward, done, info = env.step(action)

        bdi_agent.update_beliefs(obs, info={})
        next_state = bdi_agent.beliefs

        rl_agent.update(state, intention, reward, next_state)
        state = next_state

        env.render()


    with open(q_table_path, "wb") as f:
        pickle.dump(rl_agent.q_table, f)
    print("[INFO] Q-table salva.")

    env.close()

if __name__ == '__main__':
    main()