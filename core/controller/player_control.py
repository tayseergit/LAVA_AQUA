import pygame
from core.component.symbols import DIRECTION, SYMBOLS
import time

class HumanPlayer:
    def __init__(self, state, actions, result, display, symbol=SYMBOLS["PLAYER"]):
        self.display = display
        self.symbol = symbol
        self.state = state
        self.actions = actions
        self.result = result

    def handle_events(self):
        """Process keyboard events to move player."""
        keys = pygame.key.get_pressed()
        available = self.actions.available_actions()

        if keys[pygame.K_UP] and "UP" in available:
            self.result.update_environment_and_player(DIRECTION["UP"])
        elif keys[pygame.K_DOWN] and "DOWN" in available:
            self.result.update_environment_and_player(DIRECTION["DOWN"])
        elif keys[pygame.K_LEFT] and "LEFT" in available:
            self.result.update_environment_and_player(DIRECTION["LEFT"])
        elif keys[pygame.K_RIGHT] and "RIGHT" in available:
            self.result.update_environment_and_player(DIRECTION["RIGHT"])

    def run(self):
        """Main loop using Pygame to move player and render GUI."""
        running = True
        while running and not self.state.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            self.handle_events()       # move player based on key press
            self.display.update_display()  
        # time.sleep(1)  # wait for 5 seconds
