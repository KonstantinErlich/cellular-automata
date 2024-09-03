import random
import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def running_in_terminal():
    """Determine if the script is running in a terminal or an IDE."""
    # Check if sys.stdin is a terminal
    return sys.stdin.isatty() and sys.stdout.isatty()


# Use TkAgg backend only if running in a terminal
if running_in_terminal():
    matplotlib.use('TkAgg')


class Automata:
    def __init__(self):
        self.width = 0
        self.steps = 0
        self.starting_state = 1
        self.starting_label = ""
        self.probability = 0
        self.state_to_label = {1: "L", 2: "M", 3: "R"}

        self.rule_map = self.build_rule_map()
        self.parameters()
        self.rule_selection()
        self.plot_grid(
            save_path=f"rule-{self.code}-{self.width}x{self.steps}-{self.starting_label}-P{self.probability}.png")

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
                self.starting_state = int(input("Where to start? 1: left corner, 2: middle, 3: right corner "))
                if self.starting_state in self.state_to_label:
                    self.starting_label = self.state_to_label[self.starting_state]
                    break
                else:
                    print("Invalid input, please try again.")
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
        starting_positions = {
            1: 0,  # Left corner
            2: self.width // 2,  # Middle
            3: self.width - 1  # Right corner
        }
        self.grid[0, starting_positions[self.starting_state]] = 1

    def condition(self, i, j, a, b, c):
        # the indexes in grid[i,j] mean the following:
        # i is the time step, goes down in the plot.
        # j is the position of the cell, j+1 is right neighbor, j-1 is left neighbor
        return self.grid[i - 1, j - 1] == a and self.grid[i - 1, j] == b and self.grid[i - 1, j + 1] == c

    def plot_grid(self, save_path=None):
        plt.figure(figsize=(40, 40))
        plt.imshow(self.grid, cmap='binary', interpolation='nearest')
        plt.title(f"1D Cellular Automaton - rule {self.code} - Probablity: {self.probability}", fontsize=50)
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

    def rule_selection(self):
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
                    self.grid[i, j] = int(random.random() < self.probability)

    # RULES:
    def rule_1(self, i, j):
        return self.condition(i, j, 0, 0, 0)

    def rule_2(self, i, j):
        return self.grid[i - 1, j + 1] != 0

    def rule_3(self, i, j):
        return self.grid[i - 1, j - 1] == 0 and self.grid[i - 1, j] == 0

    def rule_22(self, i, j):
        return (self.condition(i, j, 0, 1, 0) or
                self.condition(i, j, 0, 0, 1) or
                self.condition(i, j, 1, 0, 0))

    def rule_45(self, i, j):
        return (self.condition(i, j, 1, 0, 1) or
                self.condition(i, j, 0, 1, 1) or
                self.condition(i, j, 0, 1, 0) or
                self.condition(i, j, 0, 0, 0))

    def rule_86(self, i, j):
        return (self.condition(i, j, 1, 1, 0) or
                self.condition(i, j, 1, 0, 0) or
                self.condition(i, j, 0, 1, 0) or
                self.condition(i, j, 0, 0, 1))

    def rule_107(self, i, j):
        return (self.condition(i, j, 1, 1, 0) or
                self.condition(i, j, 1, 0, 1) or
                self.condition(i, j, 0, 1, 1) or
                self.condition(i, j, 0, 0, 1) or
                self.condition(i, j, 0, 0, 0))

    def rule_105(self, i, j):
        return (self.condition(i, j, 1, 1, 0) or
                self.condition(i, j, 1, 0, 1) or
                self.condition(i, j, 0, 1, 1) or
                self.condition(i, j, 0, 0, 0))

    def rule_225(self, i, j):
        return (self.condition(i, j, 1, 1, 1) or
                self.condition(i, j, 1, 1, 0) or
                self.condition(i, j, 1, 0, 1) or
                self.condition(i, j, 0, 0, 0))


ca = Automata()
