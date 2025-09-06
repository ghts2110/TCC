# actions.py
import time
import numpy as np

# Ordem dos botões no Genesis (gym-retro):
# [B, A, MODE, START, UP, DOWN, LEFT, RIGHT, C, Y, X, Z]
BTN = {
    "B": 0, "A": 1, "MODE": 2, "START": 3,
    "UP": 4, "DOWN": 5, "LEFT": 6, "RIGHT": 7,
    "C": 8, "Y": 9, "X": 10, "Z": 11,
}


def spam_start_for_seconds(steps, env):
    """
    Fica alternando START ON/OFF por 'seconds' segundos e depois retorna.
    - on_frames: quantos frames segurar START ligado
    - off_frames: quantos frames ficar solto entre os taps
    """

    if steps < 1000:
        if steps % 2 == 0:
            return [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        else:
            return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    return env.action_space.sample() 

    