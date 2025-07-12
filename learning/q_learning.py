import random
from collections import defaultdict

class QLearningAgent:
    def __init__(self, actions, alpha=0.1, gamma=0.95, epsilon=0.1):
        self.q_table = defaultdict(lambda: defaultdict(float))
        self.actions = actions              
        self.alpha = alpha                  
        self.gamma = gamma                  
        self.epsilon = epsilon             

    def choose_action(self, state):
        """Escolhe ação com política ε-greedy."""
        if random.random() < self.epsilon:
            return random.choice(self.actions)

        q_values = self.q_table[state]
        return max(q_values, key=q_values.get, default=random.choice(self.actions))
    
    def update(self, state, action, reward, next_state):
        """Atualiza Q-table com a fórmula de Q-learning."""
        max_future_q = max(self.q_table[next_state].values(), default=0.0)
        old_q = self.q_table[state][action]

        self.q_table[state][action] += self.alpha * (
            reward + self.gamma * max_future_q - old_q
        )
