from copy import deepcopy
from core.component.symbols import DIRECTION, SYMBOLS


class GameState:
    def __init__(self, map_data):
        self.map_data = deepcopy(map_data)
        self.initial_map = deepcopy(map_data)
        self.history = []

        # Dimensions
        self.rows = len(self.map_data)
        self.cols = len(self.map_data[0]) if self.rows > 0 else 0

        # Player & Goal
        self.player_pos = self.find_symbol(SYMBOLS["PLAYER"])
        self.initial_player_pos = deepcopy(self.player_pos)

        self.goal_pos = self.find_symbol(SYMBOLS["GOAL"])

        # Bonus counters
        self.bunus_count = self.count_bonuses()
        self.bunus_count_player = 0

        # Flags
        self.is_goal = False
        self.game_over = False

    # ======================================================
    # FIND SYMBOL
    # ======================================================
    def find_symbol(self, symbol):
        for y, row in enumerate(self.map_data):
            for x, cell in enumerate(row):
                if cell == symbol:
                    return (y, x)
        return None

    # ======================================================
    # COUNT BONUSES
    # ======================================================
    def count_bonuses(self):
        return sum(
            1
            for row in self.map_data
            for cell in row
            if cell in SYMBOLS["BUNUS"]
        )

    # ======================================================
    # PURE GOAL CHECK — BFS USES THIS
    # ======================================================
    @staticmethod
    def is_goal_status(state):
        py, px = state.player_pos
        gy, gx = state.goal_pos
        tile = state.map_data[py][px]

        # print(state.bunus_count_player , state.bunus_count)
        # Lose if step on fire
        if tile == SYMBOLS["FIRE"]:
            return False

        # Goal if reach goal & have all bonuses
        if (py, px) == (gy, gx) and state.bunus_count_player == state.bunus_count:
            return True

        # Normal
        return None

    # ======================================================
    # INTERNAL UPDATE AFTER MOVE (not BFS)
    # ======================================================
    def update_state(self, new_map):
        # Save old state for undo
        self.history.append((deepcopy(self.map_data), deepcopy(self.player_pos)))

        self.map_data = deepcopy(new_map)
        self.rows = len(self.map_data)
        self.cols = len(self.map_data[0])

        # Evaluate goal / lose states
        goal_status = GameState.is_goal_status(self)
        # print(goal_status)
        if goal_status :
            self.is_goal = True
            self.game_over = True
            print("You win! Player reached the goal.")
        elif goal_status is False:
            self.is_goal = False
            self.game_over = True
            print("You lose! Player stepped on fire.")
        else:
            self.is_goal = False
            self.game_over = False

        self.print_map()

    # ======================================================
    # UNDO
    # ======================================================
    def undo(self):
        if len(self.history) <= 1:
            print("No previous state to undo.")
            return

        last_map, last_player = self.history.pop()

        self.map_data = deepcopy(last_map)
        self.player_pos = deepcopy(last_player)
        self.rows = len(self.map_data)
        self.cols = len(self.map_data[0])

        # Re-evaluate state after undo
        status = GameState.is_goal_status(self)
        self.is_goal = (status == "goal")
        self.game_over = (status == "goal" or status == "lose")

        print("Undo performed.")
        self.print_map()

    # ======================================================
    # RESTART
    # ======================================================
    def restart(self):
        self.map_data = deepcopy(self.initial_map)
        self.player_pos = deepcopy(self.initial_player_pos)

        self.history.clear()

        self.is_goal = False
        self.game_over = False

        self.bunus_count_player = 0
        self.bunus_count = self.count_bonuses()

        print("🔁 Game restarted.")
        self.print_map()


    def is_dead_state(state):
        if not state.player_pos:
            return True  # No player found

        y, x = state.player_pos

        # Directions to check
        for dy, dx in DIRECTION.values():
            ny, nx = y + dy, x + dx

            if 0 <= ny < state.rows and 0 <= nx < state.cols:
                target = state.map_data[ny][nx]

                # If there is at least one moveable cell, it's not dead
                if target in (SYMBOLS["EMPTY"], SYMBOLS["FIRE"], SYMBOLS["WATER"]) \
                   or target in SYMBOLS["BUNUS"] \
                   or target == SYMBOLS["GOAL"] \
                   or target == SYMBOLS["SINGLE_WALL"]:  # movable wall
                    return False

        # All neighboring cells are blocked/unmovable → dead state
        return True
    
    def copy(self):
        new = GameState.__new__(GameState)
        new.map_data = [row[:] for row in self.map_data]   # shallow clone of grid
        new.player_pos = self.player_pos
        new.bunus_count_player = self.bunus_count_player
        new.rows = self.rows
        new.cols = self.cols
        new.is_goal = self.is_goal
        new.game_over = self.game_over
        return new

    # ======================================================
    # PRINT MAP
    # ======================================================
    def print_map(self):
        for row in self.map_data:
            print("".join(row))
        print()
