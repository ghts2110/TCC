import os

base_path = os.path.dirname(__file__)

rom = base_path + "/../roms/super-mario-bros.nes"

actions = [
    ['NOOP'],            #0
    ['right'],           #1
    ['left'],            #2
    ['down'],            #3
    ['up'],              #4
    ['A'],               #5
    ['B'],               #6
    ['start'],           #7
    ['select'],          #8
]