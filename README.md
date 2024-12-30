![Robot Path Navigation](https://github.com/aadhamashraf/Robot-Path-Planning/raw/main/Robot%20Path%20Navigation.gif)

# AI Maze Solver Project

This project implements various pathfinding algorithms to solve mazes. It provides a graphical user interface (GUI) to visualize the maze, the solution path, and a comparison of different algorithms.

## Project Structure

The project is organized into the following directories:

### `src/algorithms`

This directory contains the implementations of various pathfinding algorithms.

*   **`base_search.py`**:
    *   Defines an abstract base class `BaseSearch` that provides a template for all search algorithms.
    *   Includes methods for timer management, and checking for valid positions.
*   **`genetic_algorithm`**:
    *   **`genetic_algorithm.py`**: Implements a genetic algorithm to find a path through the maze using a population-based approach.
*   **`informed`**:
    *   **`astar.py`**: Implements the A* search algorithm, which uses a heuristic to guide the search and find the shortest path.
    *   **`greedy_bfs.py`**: Implements the Greedy Best-First Search algorithm, which uses a heuristic to prioritize nodes closer to the goal.
*   **`local`**:
    *   **`hill_climbing.py`**: Implements the Hill Climbing algorithm, a local search algorithm that moves to the best neighbor until a solution is found.
    *   **`simulated_annealing.py`**: Implements the Simulated Annealing algorithm, a probabilistic technique to escape local optima during pathfinding.
*   **`uninformed`**:
    *   **`bfs.py`**: Implements Breadth-First Search (BFS), which explores all neighbors at the current depth before moving to the next level.
    *   **`dfs.py`**: Implements Depth-First Search (DFS), which explores as far as possible along each branch before backtracking.
    *   **`ids.py`**: Implements Iterative Deepening Search (IDS), a strategy combining DFS with a depth limit that increases with each iteration.
    *   **`ucs.py`**: Implements Uniform Cost Search (UCS), which explores the graph based on the cost of each path.

### `src/core`

This directory contains core components for the project.

*   **`algorithm_manager.py`**: Manages the execution of search algorithms. Responsible for running the search and exporting frontier data and saving time and step information.
*   **`frontier_exporter.py`**: Responsible for exporting the frontier of explored nodes of different algorithms into text files in the `frontiers` directory.
*   **`game_state.py`**: Manages the overall state of the game, including the maze, start and goal positions, and the solution path. This class stores data between the algorithms and UI. It also manages the level used for `IDS`.
*   **`metrics.py`**: Provides various distance metrics used for pathfinding algorithms like Manhattan and Euclidean distances.
*   **`metrics_comparison.py`**: Implements functionality to visualize and compare performance metrics of different search algorithms in the form of a graph.

### `src/environment`

This directory manages the maze environment, rendering, and assets.

*   **`mazeSetup.py`**: Sets up the maze creation, and includes a function to draw the grid on the screen.
*   **`maze_generator.py`**: Responsible for generating random mazes using a randomized depth first search and also making sure the maze is solvable.
*    **`maze_renderer.py`**: Renders the maze, robot, and flag icons on the screen.
*   **`assets`**:
    *   Contains audio, robot, and flag assets for the project.

### `src/ui`

This directory manages the user interface elements.

*   **`button.py`**: Defines the `Button` class for creating interactive buttons in the UI.
*   **`button_manager.py`**: Manages all buttons, handling clicks and drawing. Provides a way to add, handle click events, and draw buttons on the screen.
*   **`game_window.py`**: Sets up the main game window, including handling events and drawing the maze, buttons, and more. Provides methods for setting audio, updating window title, handling events, drawing game, and updating title.

### `src/utilities`

This directory contains utility files.

*   **`constants.py`**: Defines various constants used throughout the project, such as screen dimensions, colors, button layouts, and directions.
*   **`metrics.py`**: Defines helper methods to calculate metrics.

## Functionality

The project allows users to:

*   Generate and visualize random mazes.
*   Solve mazes using various pathfinding algorithms (BFS, DFS, UCS, IDS, Greedy BFS, A*, Hill Climbing, Simulated Annealing, Genetic Algorithm , Q-Learning Algorithm).
*   View the solution path and see how the algorithms explore the maze.
*   Compare the performance of different algorithms in terms of execution time and number of steps using a graph.
*   Export the explored frontier of different algorithms.
*   Reset the path, reset the maze, and modify level to explore with `IDS`

## How to Run


1.  Clone the repository `https://github.com/aadhamashraf/Robot-Path-Planning.git`.
2.  Navigate to the project directory `cd <project-directory>`.
3.  Ensure you have Python 3.6+ installed. Then, install the required libraries by running `pip install -r requirements.txt`
4.  Run the `main.py` file using: `python main.py`.
