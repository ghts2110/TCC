import numpy as np

from src.mario_view import CustomMarioView

class Beliefs():
    def __init__(self):
        self.view = CustomMarioView()
        
    def extract_beliefs(self, obs, info):
        beliefs = {}

        mario_pos = self.view.find_mario(obs)
        beliefs["mario_found"] = mario_pos is not None

        if mario_pos:
            mx, my = mario_pos

            region = obs[my:my+40, mx+16:mx+56]
            beliefs["region_mean_brightness"] = np.mean(region)

            obstacle_beliefs = self.view.detect_obstacle_ahead(obs, (mx, my))
            beliefs.update(obstacle_beliefs)

        beliefs["on_ground"] = info.get("status", "") in ["small", "big", "fireball"]

        return beliefs
