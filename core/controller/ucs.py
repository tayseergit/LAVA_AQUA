from heapq import heappush, heappop
from itertools import count
import time
import pygame

from core.component.symbols import *
from core.states import *
from core.controller.solver_runner import visualize_solver_path

class UCS:
    def __init__(self, state, actions, result_class, display):
        self.initial_state = state
        self.actions = actions
        self.result_class = result_class
        self.display = display

        self.visited_states = 0
        self.generated_states = 0
        self.timeAlog = 0
 


    def ucs(self):
        start_time = time.time()
        pq = []
        start_cost = 0
        heappush(pq, (start_cost, [], self.initial_state))
        fineState = {make_key(self.initial_state): start_cost}
        while pq:
            cost, path, state = heappop(pq)
            self.visited_states += 1
            if GameState.is_goal_status(state):
                self.timeAlog = time.time() - start_time
                return path, cost
            for action in self.actions.available_actions(state):
                dy, dx = DIRECTION[action]
                ns = copy_state(state)
                ns = self.result_class().update_environment_and_player(ns, (dy, dx))
                if ns is None:
                    continue
                key = make_key(ns)
                newCost = cost +1+ count_fire(ns)
                # if key not in best_cost or new_cost < best_cost[key]:
                if key not in fineState or newCost < fineState[key]:
                    fineState[key] = newCost
                    heappush(pq, (newCost, path + [action], ns))
                    self.generated_states += 1
        self.timeAlog = time.time() - start_time
        return [], 0


    def run(self):
        path, cost = self.ucs()
        visualize_solver_path(
            path=path,
            initial_state=self.initial_state,
            result_class=self.result_class,
            display=self.display,
            solver_name="UCS",
            visited_states=self.visited_states,
            generated_states=self.generated_states,
            execution_time=self.timeAlog,
            cost=cost,
        )
