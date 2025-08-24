# src/zelda_env.py
import os
from typing import Optional
import gym
import numpy as np
import cv2
from gym.spaces import Box, Discrete
from nes_py.nes_env import NESEnv

# Mapeamento de ações NES: [right, left, down, up, start, select, B, A]
ZELDA_ACTIONS = [
    np.array([0,0,0,0,0,0,0,0]),  # 0: NOOP
    np.array([0,0,0,1,0,0,0,0]),  # 1: UP
    np.array([0,0,1,0,0,0,0,0]),  # 2: DOWN
    np.array([0,1,0,0,0,0,0,0]),  # 3: LEFT
    np.array([1,0,0,0,0,0,0,0]),  # 4: RIGHT
    np.array([0,0,0,0,0,0,0,1]),  # 5: A (sword)
    np.array([0,0,0,0,0,0,1,0]),  # 6: B (item)
    np.array([1,0,0,0,0,0,0,1]),  # 7: RIGHT + A
    np.array([0,1,0,0,0,0,0,1]),  # 8: LEFT + A
]

def pack_buttons(buttons: np.ndarray) -> np.ndarray:
    """
    Converte um vetor de 8 botões (right,left,down,up,start,select,B,A) em 1 byte.
    Retorna shape (1,) dtype=uint8, que o nes-py espera.
    """
    buttons = buttons.astype(np.uint8).tolist()
    mask = 0
    for i, v in enumerate(buttons):
        if v:
            mask |= (1 << i)  # bit i liga
    return np.array([mask], dtype=np.uint8)


def to_gray84(obs_rgb: np.ndarray) -> np.ndarray:
    # obs_rgb vem como (240, 256, 3)
    g = cv2.cvtColor(obs_rgb, cv2.COLOR_RGB2GRAY)
    g = cv2.resize(g, (84, 84), interpolation=cv2.INTER_AREA)
    return g

class ZeldaEnv(NESEnv):
    metadata = {"render.modes": ["human", "rgb_array"]}

    def __init__(self, rom_path: Optional[str] = None, frame_skip: int = 4):
        if rom_path is None:
            rom_path = os.environ.get("ZELDA_ROM", "roms/zelda.nes")
        super().__init__(rom_path=rom_path)
        self.frame_skip = frame_skip

        self.action_space = Discrete(len(ZELDA_ACTIONS))
        self.observation_space = Box(low=0, high=255, shape=(84, 84), dtype=np.uint8)

    def reset(self):
        obs_rgb = super().reset()          
        return to_gray84(obs_rgb)          

    def step(self, action_idx: int):
        total_reward = 0.0
        done = False
        info = {}
        obs_rgb = None

        buttons = ZELDA_ACTIONS[int(action_idx)]
        packed = pack_buttons(buttons)  

        for _ in range(self.frame_skip):
            obs_rgb, reward, done, info = super().step(packed)
            total_reward += float(reward)
            if done:
                break

        obs_gray = to_gray84(obs_rgb)
        return obs_gray, total_reward, done, info
