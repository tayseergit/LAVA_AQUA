# solver.py
import os
from core.actions import Actions
from core.controller.dfs_solver import DFSSolver
from core.results import Result
from data.read_map import load_map
from core.states import GameState
from core.controller.player_solver import *
from presentation.display_map import GameDisplay
from core.controller.bfs_solver import *
from core.controller.a_star import *


class Solver:
    def __init__(self, map_name):

        self.map_name = "maps2.txt"
        base_dir = os.path.dirname(__file__)
        project_root = os.path.dirname(base_dir)
        map_file = os.path.join(project_root, "data/maps_txt", map_name)
        print(os.path.abspath(map_file))

        self.map_data = load_map(map_file)
        self.state = GameState(self.map_data)
        self.actions = Actions(self.state)
        self.result = Result()     
        self.display = GameDisplay(self.state)

        self.player = HumanPlayer(self.state, self.actions, self.result, self.display)

        self.bfs = BFSSolver(self.state, self.actions, Result, self.display)
        self.dfs = DFSSolver(self.state, self.actions, Result, self.display)
        self.astar = AStarSolver(self.state, self.actions, Result,self.display)

    def solve(self):
        print("Simulation started...")
 
        # self.player.run()
        # self.dfs.run()
        # self.bfs.run()
        self.astar.run()


