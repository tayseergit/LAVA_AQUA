# solver.py
import os
from core.actions import Actions
from core.results import Result
from data.read_map import load_map
from core.states import GameState
from core.controller.player_solver import HumanPlayer
from presentation.display_map import GameDisplay
from core.controller.bfs_solver import *


class Solver:
    def __init__(self, map_name="maps1.txt"):
        self.map_name= "maps2.txt"
        base_dir = os.path.dirname(__file__)
        project_root = os.path.dirname(base_dir)
        map_file = os.path.join(project_root, "data/maps_txt", map_name)
        print(os.path.abspath(map_file))

        self.map_data = load_map(map_file)
        self.state = GameState(self.map_data)
        self.actions = Actions(self.state)
        self.result = Result(self.state)  
        self.display = GameDisplay(self.state)
        self.player = HumanPlayer(self.state, self.actions, self.result,self.display)
        self.bfs = BFSSolver(self.state, self.actions, self.result, self.display)

        # self.result.player = self.player


    def solve(self):
        print("Simulation started...")
        self.state.print_map()
        self.player.run()  
        # self.bfs.run()

