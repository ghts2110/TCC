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
            region_brightness = region.mean()

            beliefs["region_mean_brightness"] = region_brightness

        beliefs["on_ground"] = info.get("status", "") in ["small", "big", "fireball"]

        return beliefs
