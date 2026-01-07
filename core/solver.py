# solver.py
import os

from core.actions import Actions
from core.controller.a_star import AStar
from core.controller.bfs_solver import BFSSolver
from core.controller.dfs_solver import DFSSolver
from core.controller.hill_climing import hillcliming
from core.controller.player_solver import HumanPlayer
from core.controller.ucs import UCS
from core.results import Result
from core.states import GameState
from data.read_map import *
from presentation.display_map import GameDisplay


class Solver:
    def __init__(self, map_name):
        base_dir = os.path.dirname(__file__)
        project_root = os.path.dirname(base_dir)
        map_file = os.path.join(project_root, "data/maps_txt", map_name)
        print(os.path.abspath(map_file))

        self.state = GameState(load_map(map_file))
        self.actions = Actions(self.state)
        self.result = Result()
        self.display = GameDisplay(self.state)

        self.player = HumanPlayer(self.state, self.actions, self.result, self.display)
        self.bfs = BFSSolver(self.state, self.actions, Result, self.display)
        self.dfs = DFSSolver(self.state, self.actions, Result, self.display)
        self.ucs = UCS(self.state, self.actions, Result, self.display)
        self.hill = hillcliming(self.state, self.actions, Result, self.display)
        self.astr = AStar(self.state, self.actions, Result, self.display)


    def run_solver(self, solver_key: str):
        key = solver_key.lower()
        print("Simulation started...")

        if key == "b":
            self.bfs.run()
        elif key == "d":
            self.dfs.run()
        elif key == "u":
            self.ucs.run()
        elif key == "h":
            self.hill.run()
        elif key == "a":
            self.astr.run()
        else:
            raise ValueError(f"Unknown solver key '{solver_key}'. Use B, D, or U.")
