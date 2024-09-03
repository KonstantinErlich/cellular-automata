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
        self.starting_label = ""
        self.probability = 0
        self.title = ""

        self.rule_map = self.build_rule_map()
        self.parameters()
        self.interface()
        self.plot_grid(save_path=f"{self.title}-{self.width}x{self.steps}-{self.starting_label}-P{self.probability}.png")

    def parameters(self):
        while True:
            try:
                self.width = int(input("Width: "))
                if self.width <= 0 or self.width % 2 == 0:
                    print("input is not a positive odd integer.")
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
                    print("invalid input, please try again.")
                else:
                    if self.starting_state == 1:
                        self.starting_label = "L"
                    elif self.starting_state == 2:
                        self.starting_label = "M"
                    elif self.starting_state == 3:
                        self.starting_label = "R"

                    break
            except ValueError:
                print("Please enter a valid integer for the start position.")

        while True:
            try:
                self.probability = float(input("Probability: "))
                if self.probability <= 0 or self.probability > 1:
                    print("invalid input. Probability has to be >0 and <=1.")
                else:
                    break
            except ValueError:
                print("Please enter a valid float for probability.")

    def make_grid(self):
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

    def set_cell(self, i,j):
        if random.random() < self.probability:
            self.grid[i, j] = 1
        else:
            self.grid[i, j] = 0

    def plot_grid(self, save_path=None):
        plt.figure(figsize=(40, 40))
        plt.imshow(self.grid, cmap='binary', interpolation='nearest')
        plt.title(f"1D Cellular Automaton - {self.title} - Probablity: {self.probability}", fontsize=50)
        plt.xticks([])
        plt.yticks(fontsize=45)
        plt.ylabel("Steps", fontsize=50)

        if save_path:
            plt.savefig(save_path, bbox_inches='tight')

        plt.show()


    def build_rule_map(self):
        rule_map = {}
        for attr_name in dir(self):
            attr_value = getattr(self, attr_name)
            if callable(attr_value) and attr_name.startswith('rule_'):
                rule_number = attr_name[len('rule_'):]
                if rule_number.isdigit():
                    rule_map[int(rule_number)] = attr_value
        return rule_map

    def print_available_rules(self):
        rule_numbers = sorted(self.rule_map.keys())
        print("Available rules: " + ", ".join(map(str, rule_numbers)))

    def interface(self):
        self.make_grid()
        self.print_available_rules()
        while True:
            try:
                self.code = int(input("Type the number of the rule you want to plot: "))
                if self.code in self.rule_map:
                    self.loop_over_grid(self.rule_map[self.code])
                    break
                else:
                    print("Invalid value, rule not found")
            except ValueError:
                print("Please enter a valid integer")



    def loop_over_grid(self, rule):
        for i in range(1, self.steps):
            for j in range(1, self.width - 1):
                if rule(i, j):
                    self.set_cell(i, j)
    #RULES:
    def rule_1(self, i,j):
        self.title = "rule 1"
        return self.condition(i, j, 0, 0, 0)
    def rule_2(self,i, j):
        self.title = "rule 2"
        return self.grid[i - 1, j + 1] != 0
    def rule_3(self,i, j):
        self.title = "rule 3"
        return self.grid[i - 1, j - 1] == 0 and self.grid[i - 1, j] == 0

    def rule_22(self,i, j):
        self.title = "rule 22"
        return (self.condition(i, j, 0, 1, 0) or
                        self.condition(i, j, 0, 0, 1) or
                        self.condition(i, j, 1, 0, 0))

    def rule_45(self, i, j):
        self.title = "rule 45"
        return (self.condition(i, j, 1, 0, 1) or
                self.condition(i, j, 0, 1, 1) or
                self.condition(i, j, 0, 1, 0) or
                self.condition(i, j, 0, 0, 0))
    def rule_86(self, i,j):
        self.title = "rule 86"
        return (self.condition(i, j, 1, 1, 0) or
                self.condition(i, j, 1, 0, 0) or
                self.condition(i, j, 0, 1, 0) or
                self.condition(i, j, 0, 0, 1))

    def rule_107(self, i,j):
        self.title = "rule 107"
        return (self.condition(i, j, 1, 1, 0) or
                        self.condition(i, j, 1, 0, 1) or
                        self.condition(i, j, 0, 1, 1) or
                        self.condition(i, j, 0, 0, 1) or
                        self.condition(i, j, 0, 0, 0))
    def rule_105(self,i,j):
        self.title = "rule 105"
        return (self.condition(i, j, 1, 1, 0) or
                        self.condition(i, j, 1, 0, 1) or
                        self.condition(i, j, 0, 1, 1) or
                        self.condition(i, j, 0, 0, 0))
    def rule_225(self, i,j):
        self.title = "rule 225"
        return(self.condition(i, j, 1, 1, 1) or
                        self.condition(i, j, 1, 1, 0) or
                        self.condition(i, j, 1, 0, 1) or
                        self.condition(i, j, 0, 0, 0))

ca = automata()
