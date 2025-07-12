from nes_py.wrappers import JoypadSpace
import numpy as np
import random
import time
import cv2

from src.mario_agent import CustomMarioAgent
from src.mario_view import CustomMarioView
from src.mario_env import CustomMarioEnv
from utils.actions import (
    rom,
    actions,
)

def main():
    agent = CustomMarioAgent(actions)
    view = CustomMarioView()
    env = JoypadSpace(CustomMarioEnv(rom), actions)

    env.reset()

    done = True
    for step in range(10000):
        if done:
            obs = env.reset()

        # if step == 100: 
        #     cv2.imwrite("src/assets/logo_from_obs.png", cv2.cvtColor(obs, cv2.COLOR_RGB2BGR))
        #     print("Logo capturada do obs e salva em assets/logo_from_obs.png")

        if view.is_start_screen(obs):
            env.step(7)

        env.render()

        agent.update_beliefs(obs, info={})
        agent.generate_desires()
        agent.filter_intentions()

        obs, reward, done, info = env.step(agent.act())

    env.close()

if __name__ == '__main__':
    main()