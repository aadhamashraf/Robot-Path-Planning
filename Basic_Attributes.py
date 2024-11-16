from collections import deque
import heapq
import pygame
import random
import os
import time
import matplotlib.pyplot as plt
import math
plt.style.use('dark_background')

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 650
CELL_SIZE = 20
MAZE_WIDTH = SCREEN_WIDTH // CELL_SIZE - 10
MAZE_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

# PreDefined Colors for the Whole Project
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

BUTTON_COLOR = (100, 100, 250)
BUTTON_HOVER_COLOR = (50, 50, 200)

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# Buttons Settings
button_x = 1340
button_y = 10
button_width = 120
button_height = 40
button_gap = 10
