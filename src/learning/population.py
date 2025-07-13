import random
import copy
from src.learning.q_learning import QLearningAgent

def create_population(size, actions):
    """Cria uma população de agentes Q-Learning com tabelas Q vazias."""
    
    return [QLearningAgent(actions=actions) for _ in range(size)]


def evaluate_agent(agent, view, env, bdi_agent, action_map, max_steps=10000):
    """Avalia um único agente jogando um episódio completo. Retorna a recompensa total acumulada."""
    
    obs = env.reset()
    done = False
    total_reward = 0

    bdi_agent.update_beliefs(obs, info={})
    state = bdi_agent.beliefs

    for _ in range(max_steps):
        if view.is_start_screen(obs):
            env.step(7)
            continue

        intention = agent.choose_action(state)

        if isinstance(intention, list):
            intention = intention[0] if intention else "noop"

        action = action_map.get(intention, 0)

        obs, reward, done, info = env.step(action)

        env.render()

        bdi_agent.update_beliefs(obs, info={})
        next_state = bdi_agent.beliefs

        agent.update(state, intention, reward, next_state)
        state = next_state
        total_reward += reward

        if done:
            break

    return total_reward


def evaluate_population(agents, view, env, bdi_agent, action_map):
    """Avalia todos os agentes da população e retorna uma lista (agente, score)."""

    results = []
    for agent in agents:
        score = evaluate_agent(agent, view, env, bdi_agent, action_map)
        results.append((agent, score))
    return results


def mutate_agent(agent, mutation_rate=0.05):
    """Cria uma cópia mutada do agente original (leve variação nos valores da Q-table)."""

    new_agent = QLearningAgent(actions=agent.actions)
    for state, actions_q in agent.q_table.items():
        for action, value in actions_q.items():
            noise = random.uniform(-mutation_rate, mutation_rate)
            new_agent.q_table[state][action] = value + noise
    return new_agent

def next_generation(top_agent, population_size, mutation_rate=0.05):
    """Gera a próxima geração a partir do melhor agente."""

    new_agents = [mutate_agent(top_agent, mutation_rate) for _ in range(population_size - 1)]
    return [top_agent] + new_agents