from src.mario_view import CustomMarioView

class CustomMarioAgent():
    def __init__(self, action_space):
        self.action_space = action_space
        self.beliefs = {}
        self.desires = []
        self.intentions = []
        self.view = CustomMarioView()
