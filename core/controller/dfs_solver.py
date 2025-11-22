from copy import deepcopy
import pygame
import time
from core.component.symbols import *
from core.states import *

class DFSSolver:
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
    # DFS
    # =====================================================
    def dfs(self):
        start_time = time.time()

        start_state = deepcopy(self.initial_state)
        start_key = self.make_key(start_state)

        stack = [(start_state, [])]  # Use stack for DFS
        visited = {start_key}

        self.visited_states = 0
        self.generated_states = 1

        while stack:
            current_state, path = stack.pop()  # LIFO
            self.visited_states += 1

            if current_state.is_goal:
                self.execution_time = time.time() - start_time
                return path

            if current_state.game_over:
                continue

            available_actions = self.actions.available_actions(current_state)

            for action in available_actions:
                dy, dx = DIRECTION[action]
                cy, cx = current_state.player_pos
                ny, nx = cy + dy, cx + dx

                if not (0 <= ny < current_state.rows and 0 <= nx < current_state.cols):
                    continue

                new_state = deepcopy(current_state)
                result_handler = self.result_class()
                new_state= result_handler.update_environment_and_player(new_state, (dy, dx))
 
                # Pygame live update
                # self.display.update_display()
                
                if GameState.is_dead_state(new_state):
                    continue
                status = GameState.is_goal_status(new_state)
                if status  is True:
                    self.execution_time = time.time() - start_time
                    return path + [action]

                if status is False:
                    continue

                key = self.make_key(new_state)
                if key not in visited:
                    visited.add(key)
                    stack.append((new_state, path + [action]))
                    self.generated_states += 1

        # No solution
        self.execution_time = time.time() - start_time
        return []

    # =====================================================
    # Run DFS and display solution
    # =====================================================
    def run(self):
        path = self.dfs()

        print("\n===== DFS STATS =====")
        print("Visited:", self.visited_states)
        print("Generated:", self.generated_states)
        print("Length:", len(path))
        print(f"Execution Time: {self.execution_time:.6f} seconds")
        print("=====================\n")

        # Apply solution step by step
        result_handler = self.result_class()
        for action in path:
            dy, dx = DIRECTION[action]
            result_handler.update_environment_and_player(self.initial_state, (dy, dx))
            self.display.update_display()
