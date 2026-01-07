from collections import deque
from copy import deepcopy
import pygame
import time
from core.component.symbols import *
from core.states import *
from core.controller.solver_runner import visualize_solver_path

class BFSSolver:
    def __init__(self, state, actions, result_class, display):
        self.initial_state = state
        self.actions = actions
        self.result_class = result_class
        self.display = display
         


        self.visited_states = 0
        self.generated_states = 0
        self.execution_time = 0
  
 
    def bfs(self):
        start_time = time.time()

        start_state = self.initial_state
        queue = deque([(start_state, [])])

 
        visited = set()
        visited.add(make_key(start_state))

        # self.visited_states = 1
        self.generated_states = 1

        while queue:
            current_state, path = queue.popleft()   
            self.visited_states += 1
 

            available_actions = self.actions.available_actions(current_state)

            for action in available_actions:

                dy, dx = DIRECTION[action]

                new_state = copy_state(current_state)
                handler = self.result_class()
                new_state = handler.update_environment_and_player(new_state, (dy, dx))


                status = GameState.is_goal_status(new_state)

                if status:
                    self.execution_time = time.time() - start_time
                    return path + [action]

                if  status is False :
                    continue

                key = make_key(new_state)
                if key not in visited:
                    visited.add(key)
                    queue.append((new_state, path + [action]))
                    self.generated_states += 1
 
   
        self.execution_time = time.time() - start_time
        return []
 
    def run(self):
        path = self.bfs()
        visualize_solver_path(
            path=path,
            initial_state=self.initial_state,
            result_class=self.result_class,
            display=self.display,
            solver_name="BFS",
            visited_states=self.visited_states,
            generated_states=self.generated_states,
            execution_time=self.execution_time,
            
        )
       
