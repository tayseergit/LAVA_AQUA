from collections import deque
from core.component.symbols import DIRECTION

class BFSSolver:
    def __init__(self, state, actions, result, display):
        self.state = state
        self.actions = actions
        self.result = result
        self.display = display

    def find_goal(self):
        """Find coordinates of the goal cell (■)."""
        for y, row in enumerate(self.state.map_data):
            for x, cell in enumerate(row):
                if cell == "■":
                    return (y, x)
        return None

    def bfs(self):
        """Run BFS and return list of actions to reach the goal."""
        start = self.state.player_pos
        goal = self.find_goal()

        if not goal:
            print("Goal not found on map!")
            return []

        queue = deque([(start, [])])
        visited = set([start])

        moves = {
            "UP": (-1, 0),
            "DOWN": (1, 0),
            "LEFT": (0, -1),
            "RIGHT": (0, 1)
        }

        while queue:
            (y, x), path = queue.popleft()

            if (y, x) == goal:
                return path  # list of actions

            self.state.player_pos = (y, x)  # sync state for Actions
            available = self.actions.available_actions()

            for action in available:
                dy, dx = moves[action]
                ny, nx = y + dy, x + dx

                if (ny, nx) not in visited:
                    visited.add((ny, nx))
                    queue.append(((ny, nx), path + [action]))

        return []

    def run(self):
        """Execute BFS and automatically move the player."""
        path = self.bfs()

        if not path:
            print("No path found.")
            return

        print("\nBFS Path:", path)

        # Execute movements step-by-step
        for action in path:
            direction = DIRECTION[action]
            self.result.update_environment_and_player(direction)
            self.display.update_display()
