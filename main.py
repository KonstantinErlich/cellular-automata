import numpy as np
import matplotlib.pyplot as plt
import ast
import inspect


def scan_functions_in_current_file():
    # Get the current file's source code
    current_file = inspect.getsource(inspect.currentframe().f_back)

    # Parse the source code into an AST
    tree = ast.parse(current_file)

    # List to store function names that start with "rule"
    rule_functions = []

    # Iterate through the nodes of the AST
    for node in ast.walk(tree):
        # Check if the node is a function definition
        if isinstance(node, ast.FunctionDef):
            # Add the function name to the list if it starts with "rule"
            if node.name.startswith("rule"):
                rule_functions.append(node.name)

    return rule_functions

title = ""
# Parameters
width = 201  # Width of the grid (must be odd for a clear center)
steps = 200  # Number of steps

# Initialize the grid
grid = np.zeros((steps, width), dtype=int)
midpoint = width // 2
grid[0, midpoint] = 1  # Start with the middle cell black


# the indexes in grid[i,j] mean the following:
# i is the time step, goes down in the plot.
# j is the position of the cell, j+1 is right neighbor, j-1 is left neighbor

def condition(i, j, a, b, c):
    return grid[i - 1, j - 1] == a and grid[i - 1, j] == b and grid[i - 1, j + 1] == c

# rules:
def rule_1():
    global title
    title = "rule 1"
    for i in range(1, steps):
        for j in range(1, width - 1):
            if condition(i, j, 0, 0, 0):
                grid[i, j] = 1


def rule_2():
    global title
    title = "rule 2"
    for i in range(1, steps):
        for j in range(1, width - 1):
            if grid[i - 1, j + 1] != 0:
                grid[i, j] = 1


def rule_3():
    global title
    title = "rule 3"
    for i in range(1, steps):
        for j in range(1, width - 1):
            if grid[i - 1, j - 1] == 0 and grid[i - 1, j] == 0:
                grid[i, j] = 1


def rule_22():
    global title
    title = "rule 22"
    for i in range(1, steps):
        for j in range(1, width - 1):
            if (condition(i, j, 0, 1, 0) or
                    condition(i, j, 0, 0, 1) or
                    condition(i, j, 1, 0, 0)):
                grid[i, j] = 1


def rule_107():
    global title
    title = "rule 107"
    for i in range(1, steps):
        for j in range(1, width - 1):
            if (condition(i, j, 1, 1, 0) or
                    condition(i, j, 1, 0, 1) or
                    condition(i, j, 0, 1, 1) or
                    condition(i, j, 0, 0,1) or
                    condition(i, j, 0, 0, 0)):
                grid[i, j] = 1


#functionality to type rule number to plot it
print("available rules: ")
print("Found rules: " + ", ".join(scan_functions_in_current_file()).replace("rule_", ""))

while True:
    code = int(input("type the number of the rule you want to plot: "))
    match code:
        case 1:
            rule_1()
            break
        case 2:
            rule_2()
            break
        case 3:
            rule_3()
            break
        case 22:
            rule_22()
            break
        case 107:
            rule_107()
            break
        case _:
            print("invalid value, rule not found")


# Plotting the grid
plt.figure(figsize=(20, 20))
plt.imshow(grid, cmap='binary', interpolation='nearest')
plt.title(f"1D Cellular Automaton - {title}")
plt.show()
