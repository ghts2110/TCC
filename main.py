from nes_py import NESEnv
from nes_py.wrappers import JoypadSpace
import numpy as np
import os

# Caminho para a sua ROM
rom_path = "./roms/super-mario-bros.nes"  # ajuste se estiver em outro local

# Cria um ambiente diretamente com a ROM
class CustomMarioEnv(NESEnv):
    def __init__(self):
        super().__init__(rom_path)

RIGHT_ONLY = [
    ['NOOP'],
    ['right'],
    ['right', 'A'],
    ['A'],
]

env = JoypadSpace(CustomMarioEnv(), RIGHT_ONLY)

done = True
while True:
    if done:
        obs = env.reset()
         
    env.render()
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)

env.close()
