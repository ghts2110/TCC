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
            obstacles = self.view.detect_obstacle_ahead(obs, mario_pos)
            enemies = self.view.detect_enemie_ahead(obs, mario_pos)
            items = self.view.detect_item_ahead(obs, mario_pos)
            misc = self.view.detect_misc_ahead(obs, mario_pos)
            
            beliefs.update(obstacles)
            beliefs.update(enemies)
            beliefs.update(items)
            beliefs.update(misc)


            mx, my = mario_pos
            region = obs[my:my+40, mx+16:mx+56]
            beliefs["region_mean_brightness"] = np.mean(region)

        beliefs["on_ground"] = info.get("status", "") in ["small", "big", "fireball"]

        return beliefs
