from src.bdi.beliefs import Beliefs

class CustomMarioAgent():
    def __init__(self, action_space):
        self.action_space = action_space
        self.beliefs = {}
        self.desires = []
        self.intentions = []

        self.update_b = Beliefs()

    def update_beliefs(self, obs, info):
        self.beliefs = self.update_b.extract_beliefs(obs, info)
        print(f"[Beliefs] {self.beliefs}")