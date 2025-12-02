# main.py
from core.solver import Solver
from presentation.display_map import *
level ="maps12.txt"
if __name__ == "__main__":
    open(r"D:\\مشاريع\\LAVA_AQUA\\data\\states_log.txt", "w", encoding="utf-8").close()

    solver = Solver(level)
    state = solver.solve()

    # Display map from the state
