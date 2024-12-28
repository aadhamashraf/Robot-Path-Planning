import numpy as np
from src.algorithms.q_learning_algorithm.q_learning import QLearning
from src.utilities import DIRECTIONS

size = 4
grid = np.array([[1, 1, 1, 1],
                 [1, 0, 1, 0],
                 [1, 1, 1, 0],
                 [0, 1, 1, 2]]) # The Goal State Also is Fixed here as 2 This wil be also changed 


def print_grid(grid, agent_pos):
    for r, row in enumerate(grid):
        print(" ".join("A" if (r, c) == agent_pos else ("X" if cell == 0 else ("G" if cell == 2 else ".")) 
                       for c, cell in enumerate(row))
              )
    print("\n")

def main():
    q_learning = QLearning(size)
    agent_pos = (0, 0) # As we randomly intitate the agent position, for now it will start from 0 , 0 
    episode, wins = 0, 0
    max_steps, max_episodes = 99, 10000

 # This is the training phase. It should be triggered when the button is clicked
    while episode < max_episodes:
        epsilon = q_learning.get_epsilon(episode)
        if episode % 1000 == 0:
            print(f"Episode: {episode}, Epsilon: {epsilon}")

        agent_pos = (0, 0)
        steps = 0

        while steps < max_steps:
            print(f"Episode {episode}, Step {steps}")
            print_grid(grid, agent_pos)

            state = size * agent_pos[0] + agent_pos[1]
            action = q_learning.take_action(state, epsilon)

            dr, dc = DIRECTIONS[action]
            new_pos = (agent_pos[0] + dr, agent_pos[1] + dc)

            if 0 <= new_pos[0] < size and 0 <= new_pos[1] < size and grid[new_pos[0]][new_pos[1]] != 0:
                agent_pos = new_pos

            steps += 1

            if grid[agent_pos[0]][agent_pos[1]] == 0:  
                reward = -1
                break  
            elif grid[agent_pos[0]][agent_pos[1]] == 2:  
                reward = 1
                wins += 1
                break  
            else:
                reward = 0  

            next_state = size * agent_pos[0] + agent_pos[1]
            q_learning.update_q_table(state, action, reward, next_state)

        episode += 1

    print(f"Q-table after training: \n{q_learning.q_table}")
    print(f"Total Wins: {wins}")
  
  # Consider RUNNING down the method of visualizing the performance once the Q-learning training terminates 
'''
    def log_performance(self, reward, steps):
    def plot_metrics(self):
'''
if __name__ == "__main__":
    main()
