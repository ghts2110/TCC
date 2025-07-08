import cv2
import numpy as np
import os

class CustomMarioView():
    def __init__(self, threshold=0.8):
        self.threshold = threshold
    
    def is_start_screen(self, obs, template_path="src/assets/logo_mario.png"):
        """Detecta se o logo 'SUPER MARIO BROS' está presente no frame."""
        frame = cv2.cvtColor(obs, cv2.COLOR_RGB2BGR)
        result = cv2.matchTemplate(frame, cv2.imread(template_path), cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        return max_val > self.threshold
