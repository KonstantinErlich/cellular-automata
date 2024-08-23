import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sys

def running_in_terminal():
    """Determine if the script is running in a terminal or an IDE."""
    # Check if sys.stdin is a terminal
    return sys.stdin.isatty() and sys.stdout.isatty()

# Use TkAgg backend only if running in a terminal
if running_in_terminal():
    matplotlib.use('TkAgg')



class automata():
    def __init__(self):
        self.width = 0
        self.steps = 0
        self.starting_state = 1
        self.title = ""
        self.parameters()
        self.print_method_names()
        self.create()
        self.plot_grid()

    def parameters(self):
        while True:
            try:
                self.width = int(input("Width: "))
                if self.width <= 0 or self.width % 2 == 0:
                    print("Width is not a positive odd number.")
                else:
                    break
            except ValueError:
                print("Please enter a valid integer for width.")

        while True:
            try:
                self.steps = int(input("Steps: "))
                if self.steps <= 0:
                    print("Steps is not a positive integer.")
                else:
                    break
            except ValueError:
                print("Please enter a valid integer for steps.")

        while True:
            try:
                self.starting_state = int(input("where to start? 0: left corner, 1: middle, 2: right corner"))
                if self.starting_state not in [0, 1, 2]:
                    print("Starting_state is not a valid integer for starting_state.")
                else:
                    break
            except ValueError:
                print("Please enter a valid integer for starting_state.")

    def grid(self):
        self.grid = np.zeros((self.steps, self.width), dtype=int)
        self.midpoint = self.width // 2
        if self.starting_state == 0:
            self.grid[0, 0] = 1
        if self.starting_state == 1:
            self.grid[0, self.midpoint] = 1  # Start with the middle cell black
        if self.starting_state == 2:
            self.grid[0, self.width-1] = 1
    def condition(self, i, j, a, b, c):
        # the indexes in grid[i,j] mean the following:
        # i is the time step, goes down in the plot.
        # j is the position of the cell, j+1 is right neighbor, j-1 is left neighbor
        return self.grid[i - 1, j - 1] == a and self.grid[i - 1, j] == b and self.grid[i - 1, j + 1] == c

    def rule_1(self):
        global title
        title = "rule 1"
        for i in range(1, self.steps):
            for j in range(1, self.width - 1):
                if self.condition(i, j, 0, 0, 0):
                    self.grid[i, j] = 1

    def plot_grid(self):
        plt.figure(figsize=(20, 20))
        plt.imshow(self.grid, cmap='binary', interpolation='nearest')
        plt.title(f"1D Cellular Automaton - {title}")
        plt.show()


    def create(self):
        self.grid()
        while True:
            self.code = int(input("type the number of the rule you want to plot: "))
            match self.code:
                case 1:
                    self.rule_1()
                    break
                case _:
                    print("invalid value, rule not found")

    def print_method_names(self):
        method_names = []
        # Iterate over the attributes of the class
        for attr_name in dir(self):
            # Get the attribute value
            attr_value = getattr(self, attr_name)
            # Check if the attribute is callable and starts with 'rule'
            if callable(attr_value) and not attr_name.startswith('__') and attr_name.startswith('rule'):
                # Remove 'rule' prefix and add to the list
                method_names.append(attr_name[len('rule_'):])

        # Print the method names separated by commas
        print("available methods:" + ", ".join(method_names))




ca = automata()
