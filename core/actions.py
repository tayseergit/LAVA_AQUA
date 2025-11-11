from core.component.symbols import DIRECTION, SYMBOLS


class Actions:
 
    def __init__(self, state):
         
        self.state = state
 
    def get_player_position(self):
         
        for y, row in enumerate(self.state.map_data):
            for x, tile in enumerate(row):
                if tile == SYMBOLS["PLAYER"] :
                    return y, x
        return None

    def available_actions(self):
        pos = self.state.player_pos
        if not pos:
            return []
        y, x = pos
        actions = []
    
        for action, (dy, dx) in DIRECTION.items():
            new_y, new_x = y + dy, x + dx
    
            if 0 <= new_y < len(self.state.map_data) and 0 <= new_x < len(self.state.map_data[0]):
                target = self.state.map_data[new_y][new_x]
    
                # Check if target is a SINGLE_WALL and can be pushed
                if target == SYMBOLS["SINGLE_WALL"]:
                    wall_behind_y = new_y + dy
                    wall_behind_x = new_x + dx
                    if 0 <= wall_behind_y < len(self.state.map_data) and 0 <= wall_behind_x < len(self.state.map_data[0]):
                        behind_cell = self.state.map_data[wall_behind_y][wall_behind_x]
                        if behind_cell in (SYMBOLS["EMPTY"], SYMBOLS["FIRE"], SYMBOLS["WATER"]):
                            actions.append(action)  # wall can be pushed
                    continue  # skip normal movement check for SINGLE_WALL
                
                # Normal move (empty, water, fire, goal, bonus)
                if target not in (SYMBOLS["WALL"], SYMBOLS["SIMI_WALL"]) and not target.isdigit():
                    actions.append(action)
    
        return actions

    def print_available_actions(self):

        actions = self.available_actions()
        print("\nAvailable actions for player (●):")
        if actions:
            for a in actions:
                print(f" - {a}")
        else:
            print("No available moves (player is blocked).")
