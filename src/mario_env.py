from nes_py import NESEnv

class CustomMarioEnv(NESEnv):
    def __init__(self, rom):
        super().__init__(rom)