from core.component.symbols import SYMBOLS


class GameState:
    def __init__(self, map_data):
        self.map_data = map_data
        self.rows = len(map_data)
        self.cols = len(map_data[0]) if self.rows > 0 else 0
        self.player_pos = self.find_symbol(SYMBOLS["PLAYER"])
        # print (self.player_pos)
        self.goal_pos = self.find_symbol(SYMBOLS["GOAL"])  # store goal coordinates
        self.is_goal = False
        self.game_over = False
        self.bunus_count_player =0
        self.bunus_count = self.count_bonuses()

    def find_symbol(self, symbol):
        for y, row in enumerate(self.map_data):
            for x, cell in enumerate(row):
                if cell == symbol:
                    if symbol in SYMBOLS["BUNUS"]:
                        self.bunus_count+=1
                    return y, x
        return None
    

    def count_bonuses(self):
        count = 0
        for row in self.map_data:
            for cell in row:
                if cell in SYMBOLS["BUNUS"]:
                    count += 1
        return count

    def is_goal_fun(self):
        player_x, player_y = self.player_pos
        goal_x, goal_y = self.goal_pos
         # print(self.bunus_count_player)
        if self.map_data[player_x][player_y] == SYMBOLS["FIRE"]:
            self.is_goal = False
            self.game_over = True
            print("You lose! Player stepped on fire.")
        # Check win condition
        elif (player_x, player_y) == (goal_x, goal_y) and self.bunus_count == self.bunus_count_player:
            self.is_goal = True
            self.game_over = True
            print("You win! Player reached the goal.")
        else:
            self.is_goal = False
            self.game_over = False

    def update_state(self, new_map):
        self.map_data = new_map
        self.rows = len(new_map)
        self.cols = len(new_map[0]) if self.rows > 0 else 0
        self.is_goal_fun()

    def print_map(self):
        for row in self.map_data:
            print("".join(row))
        print()
