# src/algorithms/q_learning_algorithm/q_learning.py
import numpy as np
import random
import time
from src.algorithms.base_search import BaseSearch
from src.utilities.constants import DIRECTIONS, MAZE_HEIGHT, MAZE_WIDTH


class QLearning(BaseSearch):
    def __init__(self, maze, start, goal, alpha=0.7, gamma=0.95, epsilon_decay=0.00005, max_epsilon=1.2, min_epsilon=0.05):
        super().__init__(maze, start, goal)
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon_decay = epsilon_decay
        self.max_epsilon = max_epsilon
        self.min_epsilon = min_epsilon
        self.q_table = np.zeros((len(maze) * len(maze[0]), len(DIRECTIONS)))
        self.size = len(maze)
        self.episode = 0
        self.wins = 0
        self.max_steps = MAZE_HEIGHT * MAZE_WIDTH
        self.max_episodes = 15000  # Increased max episodes
        self.epsilon = 0

    def search(self):
        self._start_timer()

        while self.episode < self.max_episodes:
            self.epsilon = self.get_epsilon(self.episode)
            if self.episode % 1000 == 0:
                print(f"Episode: {self.episode}, Epsilon: {self.epsilon}")

            current = self.start
            steps = 0

            while steps < self.max_steps:
                # Convert the position to the state
                state = self.size * current[1] + current[0]
                action = self._take_action(state, self.epsilon)
                dr, dc = DIRECTIONS[action]
                new_pos = (current[0] + dr, current[1] + dc)

                if self._is_valid_position(new_pos[0], new_pos[1]):
                    current = new_pos

                steps += 1
                if current == self.goal:
                    reward = 1
                    self.wins += 1
                    break
                elif self.maze[current[1]][current[0]] == 1:
                    reward = 0
                    break
                else:
                    reward = -0.1

                next_state = self.size * current[1] + current[0]
                self._update_q_table(state, action, reward, next_state)

            self.episode += 1
            # Reset the current position to the default maze position
            self.start = self.start

        print(f"Q-table after training: \n{self.q_table}")
        print(f"Total Wins: {self.wins}")

        return self._extract_path(), [], self.episode, self._get_elapsed_time()

    def _take_action(self, state, epsilon):
        if random.random() > epsilon:
            return np.argmax(self.q_table[state])
        row, col = state // self.size, state % self.size
        valid_actions = [i for i, (dr, dc) in enumerate(DIRECTIONS) if 0 <= (
            new_row := row + dr) < self.size and 0 <= (new_col := col + dc) < self.size and self.maze[new_row][new_col] == 0]
        return random.choice(valid_actions) if valid_actions else 0

    def _update_q_table(self, state, action, reward, next_state):
        self.q_table[state][action] += self.alpha * (reward + self.gamma * np.max(
            self.q_table[next_state]) - self.q_table[state][action])

    def get_epsilon(self, episode):
        return self.min_epsilon + (self.max_epsilon - self.min_epsilon) * np.exp(-self.epsilon_decay * episode)

    def _extract_path(self):
        current = self.start
        path = [current]
        steps = 0
        while current != self.goal and steps < 1000:
            state = self.size * current[1] + current[0]
            action = np.argmax(self.q_table[state])
            dr, dc = DIRECTIONS[action]
            new_pos = (current[0] + dr, current[1] + dc)
            if self._is_valid_position(new_pos[0], new_pos[1]):
                current = new_pos
                path.append(current)
            steps += 1
        return path
