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

    # =====================================================
    # Hash key for state
    # =====================================================
    def make_key(self, state):
        map_key = tuple(tuple(row) for row in state.map_data)
        return (map_key, state.player_pos, state.bunus_count_player)

    # =====================================================
    # BFS
    # =====================================================
    def bfs(self):
        start_time = time.time()

        start_state = deepcopy(self.initial_state)
        start_key = self.make_key(start_state)

        queue = deque([(start_state, [])])     # FIFO queue for BFS
        visited = {start_key}

        self.visited_states = 0
        self.generated_states = 1

        while queue:
            current_state, path = queue.popleft()   # FIFO dequeue
            self.visited_states += 1
 
            if current_state.is_goal:
                self.execution_time = time.time() - start_time
                return path

            if current_state.game_over:
                continue

            available_actions = self.actions.available_actions(current_state)

            for action in available_actions:

                dy, dx = DIRECTION[action]

                new_state = deepcopy(current_state)
                new_state= self.result_class.update_environment_and_player(new_state, (dy, dx))
                # self.display.update_display()

               
                if GameState.is_dead_state(new_state):
                    continue
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

        # No solution
        self.execution_time = time.time() - start_time
        return []

    # =====================================================
    # Run BFS and display solution
    # =====================================================

    def run(self):
        path = self.bfs()
        result_class = self.result_class()


        for action in path:
            # Handle Pygame events to keep window responsive
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            dy, dx = DIRECTION[action]
            result_class.update_environment_and_player(self.initial_state, (dy, dx))

            self.display.update_display()  # redraw map
            time.sleep(0.1)  # small delay to visualize the movement

        # Keep the window open after finishing
        print("\n===== BFS STATS =====")
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
       
