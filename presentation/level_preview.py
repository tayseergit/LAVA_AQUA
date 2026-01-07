import os
import pygame

from core.component.symbols import SYMBOLS, COLORS
from core.states import GameState
from data.read_map import load_map


class LevelPreviewScreen:
    BG_COLOR = (10, 14, 32)
    PANEL_COLOR = (20, 24, 46)
    TEXT_COLOR = (235, 238, 255)
    HINT_COLOR = (170, 185, 210)

    def __init__(self, level_file, cell_size=50):
        presentation_dir = os.path.dirname(__file__)
        project_root = os.path.dirname(presentation_dir)
        maps_dir = os.path.join(project_root, "data", "maps_txt")
        self.map_path = os.path.join(maps_dir, level_file)
        self.level_file = level_file

        map_data = load_map(self.map_path)
        self.state = GameState(map_data)

        pygame.init()
        self.cell_size = cell_size
        self.rows = len(map_data)
        self.cols = len(map_data[0])

        self.info_height = 140
        self.window_width = self.cols * cell_size
        self.window_height = self.rows * cell_size + self.info_height

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(f"LAVA AQUA - Preview {level_file}")
        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.SysFont("bahnschrift", 36, bold=True)
        self.info_font = pygame.font.SysFont("consolas", 22)

    def _draw_map(self):
        for y, row in enumerate(self.state.map_data):
            for x, tile in enumerate(row):
                color = COLORS.get(tile, (30, 30, 60))
                rect = pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )

                if tile == SYMBOLS["PLAYER"]:
                    pygame.draw.rect(self.screen, COLORS[SYMBOLS["EMPTY"]], rect)
                elif tile == SYMBOLS["BUNUS"]:
                    pygame.draw.rect(self.screen, (220, 220, 220), rect)
                    pygame.draw.circle(self.screen, COLORS[SYMBOLS["BUNUS"]], rect.center, self.cell_size // 3 - 4)
                elif tile.isdigit():
                    pygame.draw.rect(self.screen, (0, 200, 0), rect)
                    font = pygame.font.SysFont("bahnschrift", self.cell_size // 2, bold=True)
                    text_surface = font.render(tile, True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=rect.center)
                    self.screen.blit(text_surface, text_rect)
                elif tile in (
                    SYMBOLS["SIMI_WALL"],
                    SYMBOLS["SIMI_WALL_FIRE"],
                    SYMBOLS["SIMI_WALL_WATER"],
                ):
                    if tile == SYMBOLS["SIMI_WALL_FIRE"]:
                        bg_color = COLORS[SYMBOLS["FIRE"]]
                    elif tile == SYMBOLS["SIMI_WALL_WATER"]:
                        bg_color = COLORS[SYMBOLS["WATER"]]
                    else:
                        bg_color = (200, 200, 200)
                    pygame.draw.rect(self.screen, bg_color, rect)
                else:
                    pygame.draw.rect(self.screen, color, rect)

                pygame.draw.rect(self.screen, (45, 45, 75), rect, width=1)

        if hasattr(self.state, "player_pos") and self.state.player_pos:
            py, px = self.state.player_pos
            rect = pygame.Rect(px * self.cell_size, py * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.circle(
                self.screen,
                COLORS.get(SYMBOLS["PLAYER"], (255, 255, 255)),
                rect.center,
                self.cell_size // 2 - 4,
            )

        for bunus in getattr(self.state, "bonus_positions", []):
            by, bx = bunus
            rect = pygame.Rect(bx * self.cell_size, by * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.circle(
                self.screen,
                COLORS.get(SYMBOLS["BUNUS"], (255, 255, 255)),
                rect.center,
                self.cell_size // 2 - 4,
            )

    def _draw_panel(self):
        panel_top = self.rows * self.cell_size
        panel_rect = pygame.Rect(0, panel_top, self.window_width, self.info_height)
        pygame.draw.rect(self.screen, self.PANEL_COLOR, panel_rect)

        title = self.title_font.render(f"Previewing {self.level_file}", True, self.TEXT_COLOR)
        self.screen.blit(title, (20, panel_top + 10))

        instructions = [
            "Press B for BFS, D for DFS, U for UCS.",
            "Press ESC to return to the level grid.",
        ]
        for idx, line in enumerate(instructions):
            text_surface = self.info_font.render(line, True, self.HINT_COLOR)
            self.screen.blit(text_surface, (20, panel_top + 60 + idx * 30))

    def run(self):
        key_map = {
            pygame.K_b: "b",
            pygame.K_d: "d",
            pygame.K_u: "u",
            pygame.K_h: "h",
            pygame.K_a: "a",
        }

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.quit()
                        return None
                    if event.key in key_map:
                        pygame.display.quit()
                        return key_map[event.key]

            self.screen.fill(self.BG_COLOR)
            self._draw_map()
            self._draw_panel()

            pygame.display.flip()
            self.clock.tick(30)
