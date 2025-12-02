# actions.py
from core.component.symbols import DIRECTION, SYMBOLS

class Actions:
    def __init__(self, state=None):
 
        self.state = state

    def available_actions(self, state=None):
     
        if state is None:
            state = self.state

        if not state or not state.player_pos:
            return []

        y_player, x_player = state.player_pos
        actions = []

        for action, (dy, dx) in DIRECTION.items():
            new_y, new_x = y_player + dy, x_player + dx

            if 0 <= new_y < state.rows and 0 <= new_x < state.cols:
                target = state.map_data[new_y][new_x]

                if target == SYMBOLS["SINGLE_WALL"]:
                    wall_behind_y = new_y + dy
                    wall_behind_x = new_x + dx
                    if 0 <= wall_behind_y < state.rows and 0 <= wall_behind_x < state.cols:
                        behind_cell = state.map_data[wall_behind_y][wall_behind_x]
                        if behind_cell in (SYMBOLS["EMPTY"], SYMBOLS["FIRE"], SYMBOLS["WATER"],SYMBOLS["BUNUS"]):
                            actions.append(action)
                    continue 

                if target not in (SYMBOLS["WALL"], SYMBOLS["SIMI_WALL"]) and not target.isdigit():
                    actions.append(action)

        return actions

    def print_available_actions(self, state=None):
 
        actions = self.available_actions(state)
        print("\nAvailable actions for player (●):")
        if actions:
            for a in actions:
                print(f" - {a}")
        else:
            print("No available moves (player is blocked).")
