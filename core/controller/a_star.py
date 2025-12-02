from heapq import heappush, heappop
from itertools import count
import time
import pygame

from core.component.symbols import *
from core.states import *

class AStarSolver:
    def __init__(self, state, actions, result_class, display):
        self.initial_state = state
        self.actions = actions
        self.result_class = result_class
        self.display = display

        self.visited = set()
        self.counter = count()  
        self.visited_states = 0
        self.generated_states = 0
        self.execution_time = 0
 
    def make_key(self, state):
        return (
            state.player_pos,
            state.bunus_count_player,
            tuple(tuple(r) for r in state.map_data)
        )
 
    def heuristic(self, state):
        py, px = state.player_pos
        gy, gx = state.goal_pos

        h = abs(py - gy) + abs(px - gx)

        danger_fire = 0
        for action in self.actions.available_actions(state):
            dy,dx =DIRECTION[action]
            ny, nx = py + dy, px + dx
            if 0 <= ny < state.rows and 0 <= nx < state.cols:
                cell = state.map_data[ny][nx]
                if cell in FIRE_SYMBOLS:
                    danger_fire += 5
                elif cell in WATER_SYMBOLS:
                    danger_fire += 1

        h -= state.bunus_count_player * 2

        return h + danger_fire


    def astar(self):
        start_time = time.time()

        start = self.initial_state
        start_g = 0
        start_f = start_g + self.heuristic(start)

        pq = []
        heappush(pq, (start_f, start_g, next(self.counter), start, []))

        start_key = self.make_key(start)
        self.visited.add(start_key)
        self.visited_states = 1
        self.generated_states = 1

        while pq:
            _, g, _, state, path = heappop(pq)

            if GameState.is_goal_status(state):
                self.execution_time = time.time() - start_time
                return path

            self.visited_states += 1

            for action in self.actions.available_actions(state):
                dy, dx = DIRECTION[action]

                new_state = copy_state(state)
                handler = self.result_class()
                new_state = handler.update_environment_and_player(new_state, (dy, dx))

                status = GameState.is_goal_status(new_state)

                if status:
                    self.execution_time = time.time() - start_time
                    return path + [action]

                if status is False:
                    continue

                key = self.make_key(new_state)

                if key not in self.visited:
                    self.visited.add(key)
                    new_g = g + 1
                    new_f = new_g + self.heuristic(new_state)

                    heappush(pq, (new_f, new_g, next(self.counter), new_state, path + [action]))
                    self.generated_states += 1

        self.execution_time = time.time() - start_time
        return []


    def run(self):
        path = self.astar()

        result_class = self.result_class()

        for action in path:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            dy, dx = DIRECTION[action]
            result_class.update_environment_and_player(self.initial_state, (dy, dx))

            self.display.update_display()
            time.sleep(0.1)

        # Stats
        print("\n===== A* STATS =====")
        print("Visited:", self.visited_states)
        print("Generated:", self.generated_states)
        print("Length:", len(path))
        print(f"Execution Time: {self.execution_time:.6f} seconds")
        print("=====================\n")

        # keep window open
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            self.display.update_display()
