from src.bdi.beliefs import Beliefs

class CustomMarioAgent():
    def __init__(self, action_space):
        self.action_space = action_space
        self.beliefs = {}
        self.desires = []
        self.intentions = []

        self.update_b = Beliefs()
        self.jump_frames_left = 0


    def update_beliefs(self, obs, info):
        # self.beliefs = self.update_b.extract_beliefs(obs, info)

        self.beliefs = self.update_b.extract_binary_beliefs(obs, info)
        print(self.beliefs)


    def generate_desires(self):
        self.desires = []

        if not self.beliefs.get("mario_found"):
            return
        
        self.desires.append("reach_goal")

        if any(enemy in key and self.beliefs[key] for key in self.beliefs for enemy in ["goomba", "koopa"]):
            self.desires.append("avoid_enemy")

        if any(obs in key and self.beliefs[key] for key in self.beliefs for obs in ["pipe_top", "block", "pipe-middle"]):
            self.desires.append("jump_over_obstacle")

        if any(it in key and self.beliefs[key] for key in self.beliefs for it in ["flower", "g_mushroom", "coin", "star", "l_mushrrom", "item"]):
            self.desires.append("collect_item")

        if self.beliefs.get("region_mean_brightness", 255) < 40:
            self.desires.append("proceed_cautiously")

        # print(self.desires)


    def filter_intentions(self):
        self.intentions = []

        if not self.desires:
            self.intentions.append("noop")
            return

        if "avoid_enemy" in self.desires or "jump_over_obstacle" in self.desires:
            self.intentions.append("jump")
            self.jump_frames_left = 8

        if "reach_goal" in self.desires or "collect_item" in self.desires:
            self.intentions.append("move_right")

        if "proceed_cautiously" in self.desires and "jump" not in self.intentions:
            self.intentions = ["noop"]

        # print(self.intentions)

    
    def act(self):
        if self.jump_frames_left > 0:
            self.jump_frames_left -= 1
            return 5  # ['A']
        
        elif "move_right" in self.intentions:
            return 1  # ['right']
        return 0  # ['NOOP']