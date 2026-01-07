import pygame
from core.component.symbols import DIRECTION
import time

class HumanPlayer:
    def __init__(self, state, actions, result, display ):
        self.display = display
        self.state = state
        self.actions = actions
        self.result = result

    def handle_events(self):
        keys = pygame.key.get_pressed()
        available = self.actions.available_actions(self.state)

        if keys[pygame.K_UP] and "UP" in available:
            self.result.update_environment_and_player(self.state,DIRECTION["UP"])
        elif keys[pygame.K_DOWN] and "DOWN" in available:
            self.result.update_environment_and_player(self.state,DIRECTION["DOWN"])
        elif keys[pygame.K_LEFT] and "LEFT" in available:
            self.result.update_environment_and_player(self.state,DIRECTION["LEFT"])
        elif keys[pygame.K_RIGHT] and "RIGHT" in available:
            self.result.update_environment_and_player(self.state,DIRECTION["RIGHT"])

    def run(self):
        running = True
        while running and not self.state.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
            self.display.handle_top_buttons(event)
            self.handle_events()       # move player based on key press
            self.display.update_display()  
 