from copy import deepcopy
from core.component.symbols import *

class Result:
    def __init__(self, state):
        self.state = state
        self.symbol = SYMBOLS["PLAYER"]
        self.water_symbol = SYMBOLS["WATER_PLAYER"]

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
        target_cell = self.game_map[new_y][new_x]
        if target_cell == SYMBOLS["FIRE"]:
            print("🔥 Player stepped on fire! Game Over.")
            self.state.game_over =True
            self.state.is_goal = False
            # self.state.update_state(self.game_map)

            return  # stop moving
        
        if self.game_map[self.y_player][self.x_player] in (SYMBOLS["WATER"]):
            self.game_map[self.y_player][self.x_player] = SYMBOLS["WATER"]
        
        elif (self.y_player, self.x_player) == self.state.goal_pos:
            self.game_map[self.y_player][self.x_player] = SYMBOLS["GOAL"]
        
        else:
            self.game_map[self.y_player][self.x_player] = SYMBOLS["EMPTY"]
        if target_cell in SYMBOLS["BUNUS"]:
            self.state.bunus_count_player += 1
            # Remove bonus from map
            self.game_map[new_y][new_x] = SYMBOLS["EMPTY"]
        # if target_cell == SYMBOLS["WATER"]:
        #     self.symbol = self.water_symbol
    
        # Update player coordinates
        self.y_player, self.x_player = new_y, new_x
        self.game_map[new_y][new_x] = self.symbol
        self.state.player_pos = (new_y, new_x)
        self.state.update_state(self.game_map)


    def update_environment(self):
        """Main function to update all environment types."""
        old_map = deepcopy(self.game_map)

        new_map = self.fire_spread(deepcopy(old_map))
        new_map = self.water_spread(new_map)
        new_map = self.digit_decrease(new_map)

        self.game_map = new_map
        self.state.update_state(self.game_map)

    def fire_spread(self, old_map):
        new_map = deepcopy(old_map)
        directions = list(DIRECTION.values())

        for y in range(len(old_map)):
            for x in range(len(old_map[y])):
                cell = old_map[y][x]
                if cell in FIRE_SYMBOLS:
                    for dy, dx in directions:
                        new_y, new_x = y + dy, x + dx
                        if 0 <= new_y < len(old_map) and 0 <= new_x < len(old_map[new_y]):
                            target = old_map[new_y][new_x]

                            if target == SYMBOLS["SIMI_WALL"]:
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
        return new_map

    # === 💧 WATER spread ===
    def water_spread(self, old_map):
        new_map = deepcopy(old_map)
        directions = list(DIRECTION.values())

        for y in range(len(old_map)):
            for x in range(len(old_map[y])):
                cell = old_map[y][x]
                if cell in WATER_SYMBOLS:
                    for dy, dx in directions:
                        new_y, new_x = y + dy, x + dx
                        if 0 <= new_y < len(old_map) and 0 <= new_x < len(old_map[new_y]):
                            target = old_map[new_y][new_x]

                            if target  in FIRE_SYMBOLS:
                                new_map[new_y][new_x] = SYMBOLS["WALL"]
                        
                            elif target == SYMBOLS["SIMI_WALL"]:
                                new_map[new_y][new_x] = SYMBOLS["SIMI_WALL_WATER"]
                            elif target not in (
                                SYMBOLS["WALL"],
                                SYMBOLS["WATER"],
                                SYMBOLS["SINGLE_WALL"],
                                SYMBOLS["GOAL"],
                                # SYMBOLS["FIRE"],
                                SYMBOLS["SIMI_WALL_WATER"],
                            ) and not target.isdigit():
                                new_map[new_y][new_x] = SYMBOLS["WATER"]
        return new_map

    # === ⏳ NUMBER WALL countdown ===
    def digit_decrease(self, old_map):
        new_map = deepcopy(old_map)
        for y in range(len(old_map)):
            for x in range(len(old_map[y])):
                cell = old_map[y][x]
                if cell.isdigit():
                    new_value = int(cell) - 1
                    new_map[y][x] = SYMBOLS["EMPTY"] if new_value <= 0 else str(new_value)
        return new_map

    def update_environment_and_player(self, direction):
 
        if self.state.game_over:
            return   

        dy, dx = direction
        self.move(dy, dx)
        self.update_environment()
        # self.update_environment()

        # if not self.state.game_over:
