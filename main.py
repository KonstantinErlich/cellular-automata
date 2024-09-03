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
        self.start_pos = 1
        self.start_label = ""
        self.probability = 0
        self.state_to_label = {1: "L", 2: "M", 3: "R"}
        self.rules = {
            1: "000",
            2: "001",
            3: "001 000",
            22: "010 001 100",
            45: "101 011 010 000",
            86: "110 100 010 001",
            105: "110 101 011 000",
            107: "110 101 011 001 000",
            225: "111 110 101 000"
        }
        self.parameters()
        self.rule_selection()
        self.plot_grid(
            save_path=f"rule-{self.code}-{self.width}x{self.steps}-{self.start_label}-P{self.probability}.png")

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
                self.start_pos = int(input("Where to start? 1: left corner, 2: middle, 3: right corner "))
                if self.start_pos in self.state_to_label:
                    self.start_label = self.state_to_label[self.start_pos]
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
        self.grid[0, starting_positions[self.start_pos]] = 1

    def plot_grid(self, save_path=None):
        plt.figure(figsize=(40, 40))
        plt.imshow(self.grid, cmap='binary', interpolation='nearest')
        plt.title(f"1D Cellular Automaton - rule {self.code} - Probability: {self.probability}", fontsize=50)
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
        rule_numbers = sorted(self.rules.keys())
        print("Available rules: " + ", ".join(map(str, rule_numbers)))

    def rule_selection(self):
        self.make_grid()
        self.print_available_rules()
        while True:
            try:
                self.code = int(input("Type the number of the rule you want to plot: "))
                if self.code in self.rules:
                    self.loop_over_grid(self.code)
                    break
                else:
                    print("Invalid value, rule not found")
            except ValueError:
                print("Please enter a valid integer")

    def loop_over_grid(self, rule):
        for i in range(1, self.steps):
            for j in range(1, self.width - 1):
                if self.apply_rule(i,j, rule):
                    self.grid[i, j] = int(random.random() < self.probability)

    def apply_rule(self, i, j, num):
        str = self.rules[num].replace(" ", "")
        for k in range(0, len(str), 3):
             if self.condition(i, j, int(str[k]), int(str[k+1]), int(str[k+2])):
                return True

    # the indexes in grid[i,j] mean the following:
    # i is the time step, goes down in the plot.
    # j is the position of the cell, j+1 is right neighbor, j-1 is left neighbor
    def condition(self, i, j, a, b, c):
        return self.grid[i - 1, j - 1] == a and self.grid[i - 1, j] == b and self.grid[i - 1, j + 1] == c

ca = Automata()

