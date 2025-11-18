from copy import deepcopy
from core.component.symbols import *

class Result:
    def __init__(self, state):
        self.state = state
        self.water_symbol = SYMBOLS["WATER_PLAYER"]

    # ======================================================
    # PUSH WALL LOGIC
    # ======================================================
    def push_wall(self, wall_y, wall_x, dy, dx):
        new_wall_y = wall_y + dy
        new_wall_x = wall_x + dx

        if not (0 <= new_wall_y < len(self.state.map_data) and 
                0 <= new_wall_x < len(self.state.map_data[0])):
            return False

        target = self.state.map_data[new_wall_y][new_wall_x]

        # Wall can be pushed into EMPTY, FIRE, WATER
        if target not in (SYMBOLS["EMPTY"], SYMBOLS["FIRE"], SYMBOLS["WATER"]):
            return False

        # Move the wall
        self.state.map_data[new_wall_y][new_wall_x] = SYMBOLS["SINGLE_WALL"]
        self.state.map_data[wall_y][wall_x] = SYMBOLS["EMPTY"]
        return True

    # ======================================================
    # PLAYER MOVE
    # ======================================================
    def move(self, dy, dx):
        y, x = self.state.player_pos
        new_y, new_x = y + dy, x + dx

        target = self.state.map_data[new_y][new_x]

        # Case 1 — movable wall
        if target == SYMBOLS["SINGLE_WALL"]:
            if not self.push_wall(new_y, new_x, dy, dx):
                return  # cannot push
            self._move_player_to(new_y, new_x)
            return

        # Case 2 — normal cell
        self._move_player_to(new_y, new_x)

    # ======================================================
    # CORE PLAYER MOVE LOGIC
    # ======================================================
    def _move_player_to(self, new_y, new_x):
        y, x = self.state.player_pos
        target = self.state.map_data[new_y][new_x]

        # Fire → game over
        if target == SYMBOLS["FIRE"]:
            print("🔥 Player stepped on fire! Game Over.")
            self.state.game_over = True
            self.state.is_goal = False
            return

        # Restore previous player tile
        if self.state.map_data[y][x] == SYMBOLS["WATER_PLAYER"]:
            self.state.map_data[y][x] = SYMBOLS["WATER"]
        elif (y, x) == self.state.goal_pos:
            self.state.map_data[y][x] = SYMBOLS["GOAL"]
        else:
            self.state.map_data[y][x] = SYMBOLS["EMPTY"]

        # Bonus pickup
        if target in SYMBOLS["BUNUS"]:
            self.state.bunus_count_player += 1
            target = SYMBOLS["EMPTY"]

        # Update new position
        self.state.map_data[new_y][new_x] = SYMBOLS["PLAYER"]
        self.state.player_pos = (new_y, new_x)

        self.state.update_state(self.state.map_data)

    # ======================================================
    # ENVIRONMENT UPDATE
    # ======================================================
    def update_environment(self):
        old_map = deepcopy(self.state.map_data)

        new_map = self.fire_spread(deepcopy(old_map))
        new_map = self.water_spread(new_map)
        new_map = self.digit_decrease(new_map)

        self.state.map_data = new_map
        self.state.update_state(self.state.map_data)

    # ======================================================
    # FIRE
    # ======================================================
    def fire_spread(self, old_map):
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

                            elif (target not in (
                                    SYMBOLS["WALL"],
                                    SYMBOLS["FIRE"],
                                    SYMBOLS["SINGLE_WALL"],
                                    SYMBOLS["GOAL"],
                                    SYMBOLS["WATER"],
                                    SYMBOLS["SIMI_WALL_FIRE"]
                                ) and not target.isdigit()):
                                new_map[ny][nx] = SYMBOLS["FIRE"]
        return new_map

    # ======================================================
    # WATER
    # ======================================================
    def water_spread(self, old_map):
        new_map = deepcopy(old_map)
        for y in range(len(old_map)):
            for x in range(len(old_map[y])):
                if old_map[y][x] in WATER_SYMBOLS:
                    for dy, dx in DIRECTION.values():
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < len(old_map) and 0 <= nx < len(old_map[0]):
                            target = old_map[ny][nx]

                            if target in FIRE_SYMBOLS:
                                new_map[ny][nx] = SYMBOLS["WALL"]

                            elif target == SYMBOLS["SIMI_WALL"]:
                                new_map[ny][nx] = SYMBOLS["SIMI_WALL_WATER"]

                            elif (target not in (
                                    SYMBOLS["WALL"],
                                    SYMBOLS["WATER"],
                                    SYMBOLS["SINGLE_WALL"],
                                    SYMBOLS["GOAL"],
                                    SYMBOLS["SIMI_WALL_WATER"]
                                ) and not target.isdigit()):
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
    def update_environment_and_player(self, direction):
        if self.state.game_over:
            return
        
        dy, dx = direction
        self.move(dy, dx)
        self.update_environment()
