# main.py
from core.solver import Solver
from presentation.display_map import *

if __name__ == "__main__":
    solver = Solver("maps2.txt")
    state = solver.solve()

    # Display map from the state
