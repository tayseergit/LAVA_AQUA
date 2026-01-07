from heapq import heappush, heappop
from itertools import count
import time
import pygame

from core.component.symbols import *
from core.states import *
from core.controller.solver_runner import visualize_solver_path

class hillcliming:
    def __init__(self, state, actions, result_class, display):
        self.initial_state = state
        self.actions = actions
        self.result_class = result_class
        self.display = display
 
        self.visited_states = 0
        self.generated_states = 0
        self.timeAlog = 0
        
    def h(self,state):
        gy ,gx =  state.goal_pos
        py ,px =  state.player_pos

        return abs (gy-py) + abs(gx-px)

    def hill(self):
        pq = []
        best_cost = self.h(self.initial_state)
        heappush(pq, (best_cost, [], self.initial_state))
        while pq:
            _ , path, state = heappop(pq)
            if GameState.is_goal_status(state):
                return path
            for action in self.actions.available_actions(state):
                dy, dx = DIRECTION[action]
                ns = copy_state(state)
                ns = self.result_class().update_environment_and_player(ns, (dy, dx))
                if ns is None:
                    continue
                newCost =  self.h(ns)
                
                heappush(pq, (newCost, path + [action], ns))
        return [], 0


    def run(self):
        path = self.hill()
        visualize_solver_path(
            path=path,
            initial_state=self.initial_state,
            result_class=self.result_class,
            display=self.display,
            solver_name="HILL",
            visited_states=self.visited_states,
            generated_states=self.generated_states,
            execution_time=self.timeAlog,
        )
