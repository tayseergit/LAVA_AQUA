# main.py
from core.solver import Solver
from presentation.display_map import *
 
if __name__ == "__main__":
    open(r"D:\\مشاريع\\LAVA_AQUA\\data\\states_log.txt", "w", encoding="utf-8").close()

    solver = Solver("maps7.txt")
    state = solver.solve()

    # Display map from the state
