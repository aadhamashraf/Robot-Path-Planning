import numpy as np
import random
import matplotlib.pyplot as plt
from src.utilities.constants import *

# In src/algorithms/q_learning.py


class QLearning:
    def __init__(self, size, alpha=0.7, gamma=0.95, epsilon_decay=0.0005, max_epsilon=1.0, min_epsilon=0.05):
        self.size = size
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon_decay = epsilon_decay
        self.max_epsilon = max_epsilon
        self.min_epsilon = min_epsilon
        self.q_table = np.zeros((size * size, len(DIRECTIONS)))

    def take_action(self, state, epsilon):
        if random.random() > epsilon:
            return np.argmax(self.q_table[state])
        row, col = state // self.size, state % self.size
        valid_actions = [i for i, (dr, dc) in enumerate(DIRECTIONS) if 0 <= (
            new_row := row + dr) < self.size and 0 <= (new_col := col + dc) < self.size]
        return random.choice(valid_actions) if valid_actions else 0

    def update_q_table(self, state, action, reward, next_state):
        self.q_table[state][action] += self.alpha * (reward + self.gamma * np.max(
            self.q_table[next_state]) - self.q_table[state][action])

    def get_epsilon(self, episode):
        return self.min_epsilon + (self.max_epsilon - self.min_epsilon) * np.exp(-self.epsilon_decay * episode)
