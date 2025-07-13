import os
from nes_py.wrappers import JoypadSpace
import pickle

from src.learning.population import (
    create_population,
    evaluate_population,
    next_generation,
)
from src.mario_agent import CustomMarioAgent
from src.mario_view import CustomMarioView
from src.mario_env import CustomMarioEnv
from utils.actions import rom

POPULATION_SIZE = 1
GENERATIONS = 2
MUTATION_RATE = 0.05
MAX_STEPS = 5000
SAVE_PATH = "best_q_table.pkl"

def main():
    print("[INFO] Iniciando treino evolutivo com Q-Learning + BDI...")

    actions = [
        ['NOOP'], ['right'], ['left'], ['down'], ['up'],
        ['A'], ['B'], ['start'], ['select']
    ]
    
    env = JoypadSpace(CustomMarioEnv(rom), actions)
    view = CustomMarioView()
    bdi_agent = CustomMarioAgent(actions)

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

    agents = create_population(POPULATION_SIZE, actions=["noop", "jump", "move_right"])

    for gen in range(GENERATIONS):
        print(f"\n Geração {gen+1}/{GENERATIONS}")

        results = evaluate_population(agents, view, env, bdi_agent, action_map)
        results.sort(key=lambda x: x[1], reverse=True)

        best_agent, best_score = results[0]
        print(f"Melhor agente: Score = {best_score}")

        with open(SAVE_PATH, "wb") as f:
            pickle.dump(best_agent.q_table, f)
        print(f"[INFO] Q-table salva em: {SAVE_PATH}")

        agents = next_generation(best_agent, POPULATION_SIZE, mutation_rate=MUTATION_RATE)

    print("\nTreinamento finalizado.")
    env.close()

if __name__ == "__main__":
    main()
