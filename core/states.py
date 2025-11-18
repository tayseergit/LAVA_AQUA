from copy import deepcopy
from core.component.symbols import SYMBOLS

class GameState:
    def __init__(self, map_data):
        self.map_data = map_data
        self.initial_map = deepcopy(map_data)  
        self.history = []   
        
        self.rows = len(map_data)
        self.cols = len(map_data[0]) if self.rows > 0 else 0
        self.player_pos = self.find_symbol(SYMBOLS["PLAYER"])
        self.initial_player_pos = deepcopy(self.player_pos)

        self.goal_pos = self.find_symbol(SYMBOLS["GOAL"])
        self.is_goal = False
        self.game_over = False
        self.bunus_count_player = 0
        self.bunus_count = self.count_bonuses()

    
    def find_symbol(self, symbol):
        for y, row in enumerate(self.map_data):
            for x, cell in enumerate(row):
                if cell == symbol:
                    if symbol in SYMBOLS["BUNUS"]:
                        self.bunus_count += 1
                    return y, x
        return None

    def count_bonuses(self):
        return sum(cell in SYMBOLS["BUNUS"] for row in self.map_data for cell in row)


    def is_goal_fun(self):
        player_y, player_x = self.player_pos
        goal_y, goal_x = self.goal_pos

        if self.map_data[player_y][player_x] == SYMBOLS["FIRE"]:
            self.is_goal = False
            self.game_over = True
            print(" You lose! Player stepped on fire.")
        elif (player_y, player_x) == (goal_y, goal_x) and self.bunus_count == self.bunus_count_player:
            self.is_goal = True
            self.game_over = True
            print(" You win! Player reached the goal.")
        else:
            self.is_goal = False
            self.game_over = False

    # === Update state (auto-history) ===
    def update_state(self, new_map):
        # save old map to history before applying new one
        self.history.append((deepcopy(self.map_data), deepcopy(self.player_pos)))
        self.map_data = deepcopy(new_map)
        self.rows = len(new_map)
        self.cols = len(new_map[0]) if self.rows > 0 else 0
        self.is_goal_fun()
        self.print_map()

    # === Undo ===
    def undo(self):
        if self.history:
            last_map, last_player = self.history.pop()
            self.map_data = self.history.pop()
            self.map_data = deepcopy(last_map)
            self.player_pos = deepcopy(last_player)
            self.rows = len(self.map_data)
            self.cols = len(self.map_data[0])
            self.is_goal_fun()
            print(" Undo performed.")
        else:
            print(" No previous state to undo.")

    # === Restart ===
    def restart(self):
        self.map_data = deepcopy(self.initial_map)
        self.player_pos = deepcopy(self.initial_player_pos)

        self.history.clear()
        self.player_pos = self.initial_player_pos
        self.is_goal = False
        self.game_over = False
        self.bunus_count_player = 0
        self.bunus_count = self.count_bonuses()

        print("🔁 Game restarted.")
        self.print_map()


    # === Print ===
    def print_map(self):
        for row in self.map_data:
            print("".join(row))
        print()
