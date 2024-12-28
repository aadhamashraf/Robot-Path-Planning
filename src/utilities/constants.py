from typing import Tuple, List
from collections import deque
import heapq
import pygame
import random
import os
import time
import matplotlib.pyplot as plt
import math
plt.style.use('dark_background')

# Screen dimensions
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 750
CELL_SIZE = 20
MAZE_WIDTH = SCREEN_WIDTH // CELL_SIZE - 10
MAZE_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

# Colors
WHITE: Tuple[int, int, int] = (255, 255, 255)
BLACK: Tuple[int, int, int] = (0, 0, 0)
GREEN: Tuple[int, int, int] = (0, 255, 0)
RED: Tuple[int, int, int] = (255, 0, 0)
BUTTON_COLOR: Tuple[int, int, int] = (100, 100, 250)
BUTTON_HOVER_COLOR: Tuple[int, int, int] = (50, 50, 200)

# Directions for maze generation and pathfinding
DIRECTIONS: List[Tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# Button layout
BUTTON_X = 1340
BUTTON_Y = 10
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 40
BUTTON_GAP = 10
