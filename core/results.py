from copy import deepcopy
from core.component.symbols import *

class Result:
    def __init__(self, state):
        self.state = state
        self.symbol = SYMBOLS["PLAYER"]
        self.game_map = self.state.map_data
        self.y_player, self.x_player = state.player_pos

    def push_wall(self, wall_y, wall_x, dy, dx):

        new_wall_y = wall_y + dy
        new_wall_x = wall_x + dx

        if not (0 <= new_wall_y < len(self.game_map) and 0 <= new_wall_x < len(self.game_map[0])):
            return False

        target_cell = self.game_map[new_wall_y][new_wall_x]

        # Can push only into empty or fire (fire is removed)
        if target_cell not in (SYMBOLS["EMPTY"], SYMBOLS["FIRE"], SYMBOLS["WATER"]):
            print(False)
            return False

        # Move the wall
        self.game_map[new_wall_y][new_wall_x] = SYMBOLS["SINGLE_WALL"]
        self.game_map[wall_y][wall_x] = SYMBOLS["EMPTY"]
        return True

    def move(self, dy, dx):
        new_y, new_x = self.y_player + dy, self.x_player + dx

    
        target = self.game_map[new_y][new_x]

         
        
        # Movable wall
        if target == SYMBOLS["SINGLE_WALL"]:
            if not self.push_wall(new_y, new_x, dy, dx):
                return  # blocked, can't push
            # Wall pushed successfully, move player
            self._move_player_to(new_y, new_x)
            return
        elif target == SYMBOLS["SINGLE_WALL"]:
            self.state.bunus_count_player +=1
        # Normal move (empty, goal, fire)
        else:
            self._move_player_to(new_y, new_x)


   
    def _move_player_to(self, new_y, new_x):
        # Restore previous cell (goal or empty)
        
        
        if (self.y_player, self.x_player) == self.state.goal_pos:
            self.game_map[self.y_player][self.x_player] = SYMBOLS["GOAL"]
        
        else:
            self.game_map[self.y_player][self.x_player] = SYMBOLS["EMPTY"]
        target_cell = self.game_map[new_y][new_x]
        if target_cell in SYMBOLS["BUNUS"]:
            self.state.bunus_count_player += 1
            # Remove bonus from map
            self.game_map[new_y][new_x] = SYMBOLS["EMPTY"]
    
        # Update player coordinates
        self.y_player, self.x_player = new_y, new_x
        self.game_map[new_y][new_x] = self.symbol
        self.state.player_pos = (new_y, new_x)
        self.state.update_state(self.game_map)

    def update_environment(self):
        old_map = deepcopy(self.game_map)
        new_map = deepcopy(old_map)
        directions = list(DIRECTION.values())

        for y in range(len(old_map)):
            for x in range(len(old_map[y])):
                cell = old_map[y][x]

                # === 🔥 FIRE spread ===
                if cell in FIRE_SYMBOLS:
                    for dy, dx in directions:
                        new_y, new_x = y + dy, x + dx
                        if 0 <= new_y < len(old_map) and 0 <= new_x < len(old_map[new_y]):
                            target = old_map[new_y][new_x]

                            if target == SYMBOLS["SIMI_WALL"]:
                                # Fire affects the SIMI_WALL but doesn't replace it
                                new_map[new_y][new_x] = SYMBOLS["SIMI_WALL_FIRE"]
                            elif target not in (
                                SYMBOLS["WALL"],
                                SYMBOLS["FIRE"],
                                SYMBOLS["SINGLE_WALL"],
                                SYMBOLS["GOAL"],
                                SYMBOLS["WATER"],
                                SYMBOLS["SIMI_WALL_FIRE"],

                            ) and not target.isdigit():
                                new_map[new_y][new_x] = SYMBOLS["FIRE"]

                # === 💧 WATER spread ===
                elif cell in WATER_SYMBOLS:
                    for dy, dx in directions:
                        new_y, new_x = y + dy, x + dx
                        if 0 <= new_y < len(old_map) and 0 <= new_x < len(old_map[new_y]):
                            target = old_map[new_y][new_x]

                            if target == SYMBOLS["SIMI_WALL"]:
                                # Water affects the SIMI_WALL but doesn't replace it
                                new_map[new_y][new_x] = SYMBOLS["SIMI_WALL_WATER"]
                            elif target not in (
                                SYMBOLS["WALL"],
                                SYMBOLS["WATER"],
                                SYMBOLS["SINGLE_WALL"],
                                SYMBOLS["GOAL"],
                                SYMBOLS["FIRE"],
                                SYMBOLS["SIMI_WALL_WATER"],

                            ) and not target.isdigit():
                                
                                new_map[new_y][new_x] = SYMBOLS["WATER"]
                             
                            
                # === ⏳ NUMBER WALL countdown ===
                elif cell.isdigit():
                    new_value = int(cell) - 1
                    new_map[y][x] = SYMBOLS["EMPTY"] if new_value <= 0 else str(new_value)
        py, px = self.y_player, self.x_player
        new_map[py][px] = SYMBOLS["PLAYER"]
        self.game_map = new_map

    def update_environment_and_player(self, direction):
        if not isinstance(direction, tuple) or len(direction) != 2:
            raise ValueError("Direction must be a tuple like (-1, 0)")

        dy, dx = direction
        self.move(dy, dx)
        self.update_environment()
        # self._move_player_to(*self.state.player_pos)

        self.state.update_state(self.game_map)
        # self.state.print_map()
