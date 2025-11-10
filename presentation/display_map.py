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

    def draw_map(self):
        font = pygame.font.SysFont("arial", self.cell_size // 2, bold=True)

        for y, row in enumerate(self.state.map_data):
            for x, tile in enumerate(row):
                color = COLORS.get(tile, (10, 0, 50))
                rect = pygame.Rect(
                    x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size
                )

                # Draw player
                if tile == SYMBOLS["PLAYER"]:
                    pygame.draw.rect(self.screen, (220, 220, 220), rect)
                    pygame.draw.circle(self.screen, color, rect.center, self.cell_size // 2 - 5)
                elif tile == SYMBOLS["BUNUS"]:
                    pygame.draw.rect(self.screen, (220, 220, 220), rect)
                    pygame.draw.circle(self.screen, color, rect.center, self.cell_size // 3 - 5)
                # Draw number
                elif tile.isdigit():
                    pygame.draw.rect(self.screen, (30, 30, 30), rect)  # background for the number
                    text_surface = font.render(tile, True, (255, 255, 255))
                    text_rect = text_surface.get_rect(center=rect.center)
                    self.screen.blit(text_surface, text_rect)
                elif tile in (SYMBOLS["SIMI_WALL"], SYMBOLS["SIMI_WALL_FIRE"], SYMBOLS["SIMI_WALL_WATER"]):
                    # Background tint based on effect
                    if tile == SYMBOLS["SIMI_WALL_FIRE"]:
                        bg_color = COLORS[SYMBOLS["FIRE"]]
                    elif tile == SYMBOLS["SIMI_WALL_WATER"]:
                        bg_color = COLORS[SYMBOLS["WATER"]]
                    else:
                        bg_color = (200, 200, 200)  # Neutral base
                
                    # Draw background color
                    pygame.draw.rect(self.screen, bg_color, rect)
                    small_size = self.cell_size // 3
                    offsets = [
                        (0, 0),  # top-left
                        (self.cell_size - small_size, 0),  # top-right
                        (0, self.cell_size - small_size),  # bottom-left
                        (self.cell_size - small_size, self.cell_size - small_size),  # bottom-right
                    ]
                    for ox, oy in offsets:
                        small_rect = pygame.Rect(
                            x * self.cell_size + ox, y * self.cell_size + oy, small_size, small_size
                        )
                        pygame.draw.rect(self.screen, color, small_rect)

            # Draw other normal tiles
                else:
                    pygame.draw.rect(self.screen, color, rect)

            # Draw grid lines
                pygame.draw.rect(self.screen, self.line_color, rect,1 )

    def update_display(self):
        """Redraw the map once."""
        self.screen.fill((0, 0, 0))
        self.draw_map()
        pygame.display.flip()
        self.clock.tick(12)  # limit to 60 FPS


