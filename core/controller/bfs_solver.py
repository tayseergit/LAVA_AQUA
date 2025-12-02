from collections import deque
from copy import deepcopy
import pygame
import time
from core.component.symbols import *
from core.states import *

class BFSSolver:
    def __init__(self, state, actions, result_class, display):
        self.initial_state = state
        self.actions = actions
        self.result_class = result_class
        self.display = display
         


        self.visited_states = 0
        self.generated_states = 0
        self.execution_time = 0
 
 
    def make_key(self, state):
 
        map_tuple = tuple(tuple(row) for row in state.map_data)
        
        return (state.player_pos, state.bunus_count_player, map_tuple)

 
    def bfs(self):
        start_time = time.time()

        start_state = self.initial_state
        queue = deque([(start_state, [])])

 
        visited = set()
        visited.add(self.make_key(start_state))

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

                key = self.make_key(new_state)
                if key not in visited:
                    visited.add(key)
                    queue.append((new_state, path + [action]))
                    self.generated_states += 1
 
   
        self.execution_time = time.time() - start_time
        return []
 
    def run(self):
        path = self.bfs()
        result_class = self.result_class()


        for action in path:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            dy, dx = DIRECTION[action]
            result_class.update_environment_and_player(self.initial_state, (dy, dx))

            self.display.update_display()  # redraw map
            time.sleep(0.1)   
 
        print("\n===== BFS STATS  =====")
        print("Visited:", self.visited_states)
        print("Generated:", self.generated_states)
        print("Length:", len(path))
        print(f"Execution Time: {self.execution_time:.6f} seconds")
        print("=====================\n")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    
            self.display.update_display()
       
