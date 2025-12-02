from core.component.symbols import DIRECTION, SYMBOLS

 
def copy_state(state):
    new = state.__class__.__new__(state.__class__)
    
    new.map_data = [row[:] for row in state.map_data]

    
    new.player_pos = state.player_pos
    new.goal_pos = state.goal_pos
    new.bunus_count_player = state.bunus_count_player
    new.bunus_count = state.bunus_count
    new.rows = state.rows
    new.cols = state.cols
    new.is_goal = state.is_goal
    new.game_over = state.game_over

    new.bonus_positions = state.bonus_positions[:]

    new.history = []

    new.initial_map = state.initial_map
    new.initial_player_pos = state.initial_player_pos

    return new


class GameState:
    def __init__(self, map_data):

        self.map_data = [row[:] for row in map_data]
        self.initial_map = [row[:] for row in map_data]

        self.history = []
        self.bonus_positions = []

        self.rows = len(self.map_data)
        self.cols = len(self.map_data[0])

        self.player_pos = self.find_symbol(SYMBOLS["PLAYER"])
        self.initial_player_pos = self.player_pos
        self.goal_pos = self.find_symbol(SYMBOLS["GOAL"])

        self.bunus_count_player = 0
        self.bunus_count = self.count_bonuses()

        self.is_goal = False
        self.game_over = False

        self.search_trace = []
 
    def find_symbol(self, symbol):
        for y, row in enumerate(self.map_data):
            for x, cell in enumerate(row):
                if cell == symbol:
                    return (y, x)
        return None

 
    def count_bonuses(self):
        self.bonus_positions = []
        count = 0

        for y, row in enumerate(self.map_data):
            for x, cell in enumerate(row):
                if cell in SYMBOLS["BUNUS"]:
                    count += 1
                    self.bonus_positions.append((y, x))

        return count

 
    @staticmethod
    def is_goal_status(state):
        py, px = state.player_pos
        gy, gx = state.goal_pos
        tile = state.map_data[py][px]

         
        if (py, px) == (gy, gx) and state.bunus_count_player == state.bunus_count:
            state.is_goal = True
            state.game_over = False
            return True

         
        if tile in (SYMBOLS["FIRE"], SYMBOLS["WALL"]):
            state.is_goal = False
            state.game_over = True
            return False

        return None  
 
    def update_state(self, new_map):


        self.history.append((copy_state(self), self.player_pos))

        self.map_data = [row[:] for row in new_map]

        self.rows = len(self.map_data)
        self.cols = len(self.map_data[0])

        status = GameState.is_goal_status(self)

        if status is True:
            self.is_goal = True
            self.game_over = True
            # print("You win!")
        elif status is False:
            self.is_goal = False
            self.game_over = True
            # print("You lose!")
        else:
            self.is_goal = False
            self.game_over = False

        # self.print_map(self.map_data)

 
    def undo(self):
        if len(self.history) < 1:
            print("No previous state.")
            return

        old_state, old_player = self.history.pop()

        self.map_data = [row[:] for row in old_state.map_data]
        self.player_pos = old_player
        self.bunus_count_player = old_state.bunus_count_player
        self.game_over = old_state.game_over
        self.is_goal = old_state.is_goal

        print("Undo done.")
        # self.print_map()
 
    def restart(self):
        self.map_data = [row[:] for row in self.initial_map]
        self.player_pos = self.initial_player_pos

        self.history.clear()
        self.bunus_count_player = 0
        self.bunus_count = self.count_bonuses()

        self.is_goal = False
        self.game_over = False

        print("🔁 Restarted.")
        # self.print_map()

 
    def is_dead_state(state):
        if not state.goal_pos:
            return True

        y, x = state.goal_pos

        for dy, dx in DIRECTION.values():
            ny, nx = y + dy, x + dx

            if 0 <= ny < state.rows and 0 <= nx < state.cols:
                target = state.map_data[ny][nx]

                if target in (
                    SYMBOLS["EMPTY"],
                    SYMBOLS["WATER"],
                    SYMBOLS["BUNUS"],
                    SYMBOLS["GOAL"],
                    SYMBOLS["SINGLE_WALL"]
                ):
                    return False

        return True
 
    def copy(self):
        return copy_state(self)
 
    def print_map(self,map_data):
        for row in map_data:
            print("".join(row))
        print()
