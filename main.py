# main.py
from core.solver import Solver
from presentation.display_map import *

if __name__ == "__main__":
    solver = Solver("maps7.txt")
    state = solver.solve()

    # Display map from the state
