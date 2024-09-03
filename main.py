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
        self.grid = None
        self.number = None
        self.width = 0
        self.steps = 0
        self.start_pos = 1
        self.start_label = ""
        self.probability = 0
        self.n_entries = 10
        self.step_size = int((self.width - 1) / (self.n_entries - 1))
        self.state_to_label = {1: "L", 2: "M", 3: "R", 4: "10EqD", 5: "10Rand"}
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
            save_path=f"rule-{self.number}-{self.width}x{self.steps}-{self.start_label}-P{self.probability}.png")

    def parameters(self):
        while True:
            try:
                self.width = int(input("Width(positive odd integer bigger than 10): "))
                if self.width <= 0 or self.width % 2 == 0 or self.width < 10:
                    print("input is not a positive odd integer bigger than 10.")
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
                self.start_pos = int(input("Where to start? 1: left corner, 2: middle, 3: right corner, 4: 10 equidistant positions, 5:10 random entries"))
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

    def single_start_cell(self):
        starting_positions = {
            1: 0,  # Left corner
            2: self.width // 2,  # Middle
            3: self.width - 1  # Right corner
        }
        self.grid[0, starting_positions[self.start_pos]] = 1
    def equidistant_start_cell(self):
        for w in range(self.n_entries):
            self.grid[0, w*self.step_size] = 1
    def random_start_cell(self):
        entries = random.sample(range(0, self.width), self.n_entries)
        for w in entries:
            self.grid[0, w] = 1


    def plot_grid(self, save_path=None):
        plt.figure(figsize=(40, 40))
        plt.imshow(self.grid, cmap='binary', interpolation='nearest')
        plt.title(f"1D Cellular Automaton - rule {self.number} - Probability: {self.probability}", fontsize=50)
        plt.xticks([])
        plt.yticks(fontsize=45)
        plt.ylabel("Steps", fontsize=50)

        if save_path:
            plt.savefig(save_path, bbox_inches='tight')

        plt.show()

    def print_available_rules(self):
        rule_numbers = sorted(self.rules.keys())
        print("Available rules: " + ", ".join(map(str, rule_numbers)))

    def rule_selection(self):
        self.grid = np.zeros((self.steps, self.width), dtype=int)
        if self.start_pos ==4:
            self.equidistant_start_cell()
        elif self.start_pos == 5:
            self.random_start_cell()
        else:
            self.single_start_cell()

        self.print_available_rules()
        while True:
            try:
                self.number = int(input("Type the number of the rule you want to plot: "))
                if self.number in self.rules:
                    self.loop_over_grid(self.number)
                    break
                else:
                    print("Invalid value, rule not found")
            except ValueError:
                print("Please enter a valid integer")

    def loop_over_grid(self, rule_num):
        for i in range(1, self.steps):
            for j in range(1, self.width - 1):
                if self.apply_rule(i, j, rule_num):
                    self.grid[i, j] = int(random.random() < self.probability)

    def apply_rule(self, i, j, num):
        rule_code = self.rules[num].replace(" ", "")
        for k in range(0, len(rule_code), 3):
            if self.condition(i, j, int(rule_code[k]), int(rule_code[k + 1]), int(rule_code[k + 2])):
                return True

    # the indexes in grid[i,j] mean the following:
    # i is the time step, goes down in the plot.
    # j is the position of the cell, j+1 is right neighbor, j-1 is left neighbor
    def condition(self, i, j, a, b, c):
        return self.grid[i - 1, j - 1] == a and self.grid[i - 1, j] == b and self.grid[i - 1, j + 1] == c


ca = Automata()
