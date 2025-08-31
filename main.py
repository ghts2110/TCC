from nes_py.wrappers import JoypadSpace

from src.learning.population import create_population, evaluate_population
from src.mario_agent import CustomMarioAgent
from src.mario_view import CustomMarioView
from src.mario_env import CustomMarioEnv
from utils.actions import (
    rom
)


def main():
    actions = [
        ['NOOP'], ['right'], ['left'], ['down'], ['up'],
        ['A'], ['B'], ['start'], ['select']
    ]
    
    action_map = {
        "noop": 0,          # ['NOOP']
        "move_right": 1,    # ['right']
        "move_left": 2,     # ['left']
        "down": 3,          # ['down']
        "up": 4,            # ['up']
        "jump": 5,          # ['A']
        "attack": 6,        # ['B']
        "start": 7,         # ['start']
        "select": 8         # ['select']
    }
    
    env = JoypadSpace(CustomMarioEnv(rom), actions)

    view = CustomMarioView()
    bdi_agent = CustomMarioAgent(actions)

    population = create_population(size=5, actions=["noop", "jump", "move_right"])
    results = evaluate_population(population, view, env, bdi_agent, action_map)

    for i, (agent, score) in enumerate(results):
        print(f"Agente {i} → Score: {score:.2f}")

    env.close()

if __name__ == '__main__':
    main()