import sys
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

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
        self.probability = -0.9
        self.title = ""
        self.parameters()
        self.print_method_names()
        self.create()
        self.plot_grid(save_path=f"{title} - P{self.probability}.png")

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
                self.starting_state = int(input("where to start? 1: left corner, 2: middle, 3: right corner"))
                if self.starting_state not in [1, 2, 3]:
                    print("Starting_state is not a valid integer for starting_state.")
                else:
                    break
            except ValueError:
                print("Please enter a valid integer for starting_state.")

        while True:
            try:
                self.probability = float(input("Probability: "))
                if self.probability <= 0 or self.probability > 1:
                    print("Probability is not a valid float for probability. has to be >0 and <=1.")
                else:
                    break
            except ValueError:
                print("Please enter a valid float for probability.")

    def grid(self):
        self.grid = np.zeros((self.steps, self.width), dtype=int)
        self.midpoint = self.width // 2
        if self.starting_state == 1:
            self.grid[0, 0] = 1
        if self.starting_state == 2:
            self.grid[0, self.midpoint] = 1
        if self.starting_state == 3:
            self.grid[0, self.width-1] = 1
    def condition(self, i, j, a, b, c):
        # the indexes in grid[i,j] mean the following:
        # i is the time step, goes down in the plot.
        # j is the position of the cell, j+1 is right neighbor, j-1 is left neighbor
        return self.grid[i - 1, j - 1] == a and self.grid[i - 1, j] == b and self.grid[i - 1, j + 1] == c

    def set_grid(self, i,j):
        if random.random() < self.probability:
            self.grid[i, j] = 1
        else:
            self.grid[i, j] = 0

    def rule_1(self):
        global title
        title = "rule 1"
        for i in range(1, self.steps):
            for j in range(1, self.width - 1):
                if self.condition(i, j, 0, 0, 0):
                    self.set_grid(i,j)

    def rule_2(self):
        global title
        title = "rule 2"
        for i in range(1, self.steps):
            for j in range(1, self.width - 1):
                if self.grid[i - 1, j + 1] != 0:
                    self.set_grid(i,j)

    def rule_3(self):
        global title
        title = "rule 3"
        for i in range(1, self.steps):
            for j in range(1, self.width - 1):
                if self.grid[i - 1, j - 1] == 0 and self.grid[i - 1, j] == 0:
                    self.set_grid(i,j)
    def rule_45(self):
        global title
        title = "rule 45"
        for i in range(1, self.steps):
            for j in range(1, self.width - 1):
                if (self.condition(i, j, 1, 0, 1) or
                        self.condition(i, j, 0, 1, 1) or
                         self.condition(i, j, 0, 1, 0) or
                          self.condition(i, j, 0, 0, 0)):
                    self.set_grid(i,j)
    def rule_86(self):
        global title
        title = "rule 86"
        for i in range(1, self.steps):
            for j in range(1, self.width - 1):
                if (self.condition(i, j, 1, 1, 0) or
                        self.condition(i, j, 1, 0, 0) or
                        self.condition(i, j, 0, 1, 0) or
                        self.condition(i, j, 0, 0, 1)):
                    self.set_grid(i, j)
    def rule_22(self):
        global title
        title = "rule 22"
        for i in range(1, self.steps):
            for j in range(1, self.width - 1):
                if (self.condition(i, j, 0, 1, 0) or
                        self.condition(i, j, 0, 0, 1) or
                        self.condition(i, j, 1, 0, 0)):
                    self.set_grid(i,j)

    def rule_107(self):
        global title
        title = "rule 107"
        for i in range(1, self.steps):
            for j in range(1, self.width - 1):
                if (self.condition(i, j, 1, 1, 0) or
                        self.condition(i, j, 1, 0, 1) or
                        self.condition(i, j, 0, 1, 1) or
                        self.condition(i, j, 0, 0, 1) or
                        self.condition(i, j, 0, 0, 0)):
                    self.set_grid(i,j)

    def rule_105(self):
        global title
        title = "rule 105"
        for i in range(1, self.steps):
            for j in range(1, self.width - 1):
                if (self.condition(i, j, 1, 1, 0) or
                        self.condition(i, j, 1, 0, 1) or
                        self.condition(i, j, 0, 1, 1) or
                        self.condition(i, j, 0, 0, 0)):
                    self.set_grid(i,j)

    def rule_225(self):
        global title
        title = "rule 225"
        for i in range(1, self.steps):
            for j in range(1, self.width - 1):
                if (self.condition(i, j, 1, 1, 1) or
                        self.condition(i, j, 1, 1, 0) or
                        self.condition(i, j, 1, 0, 1) or
                        self.condition(i, j, 0, 0, 0)):
                    self.set_grid(i,j)


    def plot_grid(self, save_path=None):
        plt.figure(figsize=(40, 40))
        plt.imshow(self.grid, cmap='binary', interpolation='nearest')
        plt.title(f"1D Cellular Automaton - {title} - Probablity: {self.probability}", fontsize=50)
        plt.xticks([])
        plt.yticks(fontsize=45)
        plt.ylabel("Steps", fontsize=50)

        if save_path:
            plt.savefig(save_path, bbox_inches='tight')

        plt.show()



    def create(self):
        self.grid()
        while True:
            self.code = int(input("type the number of the rule you want to plot: "))
            match self.code:
                case 1:
                    self.rule_1()
                    break
                case 2:
                    self.rule_2()
                    break
                case 3:
                    self.rule_3()
                    break
                case 22:
                    self.rule_22()
                    break
                case 107:
                    self.rule_107()
                    break
                case 45:
                    self.rule_45()
                    break
                case 86:
                    self.rule_86()
                    break
                case 105:
                    self.rule_105()
                    break
                case 225:
                    self.rule_225()
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
        print("available rules:" + ", ".join(method_names))


ca = automata()
