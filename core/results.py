from copy import deepcopy
from core.component.symbols import *

class Result:
    def __init__(self):
        ...
    # ======================================================
    # PUSH WALL LOGIC
    # ======================================================
    def push_wall(self, state, wall_y, wall_x, dy, dx):
        new_wall_y = wall_y + dy
        new_wall_x = wall_x + dx

        if not (0 <= new_wall_y < state.rows and 0 <= new_wall_x < state.cols):
            return False

        target = state.map_data[new_wall_y][new_wall_x]

        # Wall can be pushed into EMPTY, FIRE, WATER
        if target not in (SYMBOLS["EMPTY"], SYMBOLS["FIRE"], SYMBOLS["WATER"],SYMBOLS["BUNUS"]):
            return False

        # Move the wall
        state.map_data[new_wall_y][new_wall_x] = SYMBOLS["SINGLE_WALL"]
        state.map_data[wall_y][wall_x] = SYMBOLS["EMPTY"]
        return True

    # ======================================================
    # PLAYER MOVE
    # ======================================================
    def move(self, state, dy, dx):
        y, x = state.player_pos
        new_y, new_x = y + dy, x + dx

        target = state.map_data[new_y][new_x]

        # Case 1 — movable wall
        if target == SYMBOLS["SINGLE_WALL"]:
            if not self.push_wall(state, new_y, new_x, dy, dx):
                return  # cannot push
            self._move_player_to(state, new_y, new_x)
            return

        # Case 2 — normal cell
        self._move_player_to(state, new_y, new_x)

    # ======================================================
    # CORE PLAYER MOVE LOGIC
    # ======================================================
    def _move_player_to(self, state, new_y, new_x):
        y, x = state.player_pos
        target = state.map_data[new_y][new_x]

        # Fire → game over
        if target == SYMBOLS["FIRE"]:
            state.game_over = True
            state.is_goal = False
            return

        if (new_y, new_x) in state.bonus_positions:
            state.bunus_count_player += 1
            state.bonus_positions.remove((new_y, new_x))
        
        # Restore previous player tile
        if state.map_data[y][x] == SYMBOLS["WATER_PLAYER"]:
            state.map_data[y][x] = SYMBOLS["WATER"]
        elif state.map_data[y][x] == SYMBOLS["WATER"]:
            state.map_data[y][x] = SYMBOLS["WATER"]
        elif (y, x) == state.goal_pos:
            state.map_data[y][x] = SYMBOLS["GOAL"]
        else:
            state.map_data[y][x] = SYMBOLS["EMPTY"]

        # Bonus pickup


        # Update new position
        state.map_data[new_y][new_x] = SYMBOLS["PLAYER"]
        state.player_pos = (new_y, new_x)
        # state.update_state(state.map_data)

    # ======================================================
    # ENVIRONMENT UPDATE
    # ======================================================
    def update_environment(self, state):
        old_map = deepcopy(state.map_data)

        new_map = self.fire_spread(state,old_map)
        new_map = self.water_spread(state,new_map)
        new_map = self.digit_decrease(new_map)

        state.map_data = new_map
        state.update_state(state.map_data)
        return state
    # ======================================================
    # FIRE
    # ======================================================
    def fire_spread(self, state,old_map):
        new_map = deepcopy(old_map)
        for y in range(len(old_map)):
            for x in range(len(old_map[y])):
                if old_map[y][x] in FIRE_SYMBOLS:
                    for dy, dx in DIRECTION.values():
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < len(old_map) and 0 <= nx < len(old_map[0]):
                            target = old_map[ny][nx]
                            if target == SYMBOLS["SIMI_WALL"]:
                                new_map[ny][nx] = SYMBOLS["SIMI_WALL_FIRE"]
                            elif target not in (
                                SYMBOLS["WALL"], SYMBOLS["FIRE"], SYMBOLS["SINGLE_WALL"],
                                SYMBOLS["GOAL"], SYMBOLS["WATER"], SYMBOLS["SIMI_WALL_FIRE"]
                            ) and not target.isdigit()  and (ny, nx)!= state.goal_pos:
                                new_map[ny][nx] = SYMBOLS["FIRE"]
        return new_map

    # ======================================================
    # WATER
    # ======================================================
    def water_spread(self,state, old_map):
        new_map = deepcopy(old_map)
        for y in range(len(old_map)):
            for x in range(len(old_map[y])):
                if old_map[y][x] in WATER_SYMBOLS:
                    for dy, dx in DIRECTION.values():
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < len(old_map) and 0 <= nx < len(old_map[0]):
                            target = old_map[ny][nx]

                            if target in FIRE_SYMBOLS and (ny, nx) != state.goal_pos :
                                new_map[ny][nx] = SYMBOLS["WALL"]
                            elif target == SYMBOLS["SIMI_WALL"]:
                                new_map[ny][nx] = SYMBOLS["SIMI_WALL_WATER"]
                            elif target not in (
                                SYMBOLS["WALL"], SYMBOLS["WATER"], SYMBOLS["SINGLE_WALL"],
                                SYMBOLS["GOAL"], SYMBOLS["SIMI_WALL_WATER"]
                            ) and not target.isdigit() and (ny, nx)!= state.goal_pos:
                                new_map[ny][nx] = SYMBOLS["WATER"]
        
        return new_map

    # ======================================================
    # DIGIT WALLS
    # ======================================================
    def digit_decrease(self, old_map):
        new_map = deepcopy(old_map)
        for y in range(len(old_map)):
            for x in range(len(old_map[y])):
                if old_map[y][x].isdigit():
                    v = int(old_map[y][x]) - 1
                    new_map[y][x] = SYMBOLS["EMPTY"] if v <= 0 else str(v)
        return new_map

    # ======================================================
    # MOVE + ENVIRONMENT UPDATE
    # ======================================================
    def update_environment_and_player(self, state, direction):
        if state.game_over:
            return
        dy, dx = direction
        self.move(state, dy, dx)
        return self.update_environment(state)
        
