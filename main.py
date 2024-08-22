import numpy as np
import matplotlib.pyplot as plt

# Parameters
width = 21  # Width of the grid (must be odd for a clear center)
steps = 20  # Number of steps

# Initialize the grid
grid = np.zeros((steps, width), dtype=int)
midpoint = width // 2


# Plotting the grid
plt.figure(figsize=(10, 10))
plt.imshow(grid, cmap='binary', interpolation='nearest')
plt.title('1D Cellular Automaton')
plt.show()