import pygame
from core.component.symbols import SYMBOLS, COLORS

class GameDisplay:
    def __init__(self, state, cell_size=50):
        self.state = state
        self.cell_size = cell_size
        self.line_color = (50, 50, 50)
        pygame.init()
        self.rows, self.cols = len(state.map_data), len(state.map_data[0])

        self.window_width = self.cols * cell_size
        self.window_height = self.rows * cell_size

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("LAVA AQUA - Player Mode")
        self.clock = pygame.time.Clock()

        self.ok_button_rect = None  # For end-screen button

    # ==================== DRAW MAP ====================

    def draw_map(self):
        font = pygame.font.SysFont("arial", self.cell_size // 2, bold=True)

        for y, row in enumerate(self.state.map_data):
            for x, tile in enumerate(row):
                color = COLORS.get(tile, (10, 0, 50))
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size,
                                   self.cell_size, self.cell_size)

                if tile == SYMBOLS["PLAYER"]:
                    pygame.draw.rect(self.screen, (220, 220, 220), rect)
                    pygame.draw.circle(self.screen, color, rect.center, self.cell_size // 2 - 5)

                elif tile == SYMBOLS["BUNUS"]:
                    pygame.draw.rect(self.screen, (220, 220, 220), rect)
                    pygame.draw.circle(self.screen, color, rect.center, self.cell_size // 3 - 5)

                elif tile.isdigit():
                    pygame.draw.rect(self.screen, (30, 30, 30), rect)
                    text_surface = font.render(tile, True, (255, 255, 255))
                    text_rect = text_surface.get_rect(center=rect.center)
                    self.screen.blit(text_surface, text_rect)

                elif tile in (SYMBOLS["SIMI_WALL"], SYMBOLS["SIMI_WALL_FIRE"], SYMBOLS["SIMI_WALL_WATER"]):
                    if tile == SYMBOLS["SIMI_WALL_FIRE"]:
                        bg_color = COLORS[SYMBOLS["FIRE"]]
                    elif tile == SYMBOLS["SIMI_WALL_WATER"]:
                        bg_color = COLORS[SYMBOLS["WATER"]]
                    else:
                        bg_color = (200, 200, 200)

                    pygame.draw.rect(self.screen, bg_color, rect)
                    small_size = self.cell_size // 3
                    offsets = [
                        (0, 0),
                        (self.cell_size - small_size, 0),
                        (0, self.cell_size - small_size),
                        (self.cell_size - small_size, self.cell_size - small_size),
                    ]
                    for ox, oy in offsets:
                        small_rect = pygame.Rect(
                            x * self.cell_size + ox,
                            y * self.cell_size + oy,
                            small_size,
                            small_size,
                        )
                        pygame.draw.rect(self.screen, color, small_rect)

                else:
                    pygame.draw.rect(self.screen, color, rect)

                # Grid lines
                pygame.draw.rect(self.screen, self.line_color, rect, 1)

    # ==================== END SCREEN ====================

    def draw_end_screen(self):
        """Display win/lose message and OK button."""
        overlay = pygame.Surface((self.window_width, self.window_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Message setup
        font_big = pygame.font.SysFont("arial", 50, bold=True)
        font_small = pygame.font.SysFont("arial", 30, bold=True)

        if self.state.is_goal:
            msg = "🏆 YOU WIN!"
            color = (0, 200, 0)
        else:
            msg = "🔥 GAME OVER!"
            color = (200, 0, 0)

        msg_surface = font_big.render(msg, True, color)
        msg_rect = msg_surface.get_rect(center=(self.window_width // 2, self.window_height // 2 - 60))
        self.screen.blit(msg_surface, msg_rect)

        # OK button
        button_text = font_small.render("OK", True, (255, 255, 255))
        button_width, button_height = 120, 60
        button_rect = pygame.Rect(
            self.window_width // 2 - button_width // 2,
            self.window_height // 2 + 20,
            button_width,
            button_height,
        )
        pygame.draw.rect(self.screen, (50, 150, 250), button_rect, border_radius=15)
        text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, text_rect)

        self.ok_button_rect = button_rect

    # ==================== MAIN UPDATE ====================

    def update_display(self):
        """Redraw the map once."""
        self.screen.fill((0, 0, 0))
        self.draw_map()

        if self.state.game_over:
            self.draw_end_screen()

        pygame.display.flip()
        self.clock.tick(12)

    # ==================== OK BUTTON HANDLER ====================

    def handle_ok_click(self, event):
        """Close the program when OK button is clicked."""
        if self.ok_button_rect and event.type == pygame.MOUSEBUTTONDOWN:
            if self.ok_button_rect.collidepoint(event.pos):
                print("👋 Game closed by user.")
                pygame.quit()
                exit()
