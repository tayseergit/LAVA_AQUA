import pygame


class LevelSelectScreen:
    COLS = 5
    ROWS = 3
    BG_COLOR = (12, 12, 28)
    CARD_COLOR = (34, 48, 86)
    CARD_ACTIVE = (80, 120, 200)
    TEXT_COLOR = (240, 240, 255)
    INSTRUCTION_COLOR = (180, 190, 210)

    def __init__(self):
        pygame.init()
        self.screen_width = 900
        self.screen_height = 540
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("LAVA AQUA - Level Select")
        self.clock = pygame.time.Clock()

        self.level_files = [f"maps{idx}.txt" for idx in range(1, 16)]
        self.selected_index = 0

        self.title_font = pygame.font.SysFont("bahnschrift", 48, bold=True)
        self.level_font = pygame.font.SysFont("bahnschrift", 28, bold=True)
        self.info_font = pygame.font.SysFont("consolas", 22, bold=False)

    def _draw_grid(self):
        margin_x = 60
        margin_y = 120
        gap_x = 20
        gap_y = 20

        card_width = (self.screen_width - 2 * margin_x - (self.COLS - 1) * gap_x) // self.COLS
        card_height = (self.screen_height - margin_y - 120 - (self.ROWS - 1) * gap_y) // self.ROWS

        for idx, level in enumerate(self.level_files):
            row = idx // self.COLS
            col = idx % self.COLS
            x = margin_x + col * (card_width + gap_x)
            y = margin_y + row * (card_height + gap_y)

            rect = pygame.Rect(x, y, card_width, card_height)
            color = self.CARD_ACTIVE if idx == self.selected_index else self.CARD_COLOR
            pygame.draw.rect(self.screen, color, rect, border_radius=12)

            label = f"Level {idx + 1}"
            text_surface = self.level_font.render(label, True, self.TEXT_COLOR)
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)

    def _draw_header(self):
        title_surface = self.title_font.render("Select a Level", True, self.TEXT_COLOR)
        self.screen.blit(title_surface, title_surface.get_rect(midtop=(self.screen_width // 2, 30)))

        info_lines = [
            "Use arrow keys to highlight a level.",
            "Press Enter to preview the level map.",
            "Inside the preview: press B / D / U to run a solver, ESC to go back.",
        ]

        for i, line in enumerate(info_lines):
            text_surface = self.info_font.render(line, True, self.INSTRUCTION_COLOR)
            self.screen.blit(text_surface, (self.screen_width // 2 - text_surface.get_width() // 2,
                                            self.screen_height - 100 + i * 28))

        selected_label = f"Current selection: Level {self.selected_index + 1} ({self.level_files[self.selected_index]})"
        selected_surface = self.info_font.render(selected_label, True, self.TEXT_COLOR)
        self.screen.blit(selected_surface, selected_surface.get_rect(center=(self.screen_width // 2, 90)))

    def _handle_navigation(self, key):
        row = self.selected_index // self.COLS
        col = self.selected_index % self.COLS

        if key == pygame.K_RIGHT:
            col = (col + 1) % self.COLS
        elif key == pygame.K_LEFT:
            col = (col - 1) % self.COLS
        elif key == pygame.K_DOWN:
            row = (row + 1) % self.ROWS
        elif key == pygame.K_UP:
            row = (row - 1) % self.ROWS

        self.selected_index = (row % self.ROWS) * self.COLS + (col % self.COLS)
        self.selected_index = max(0, min(self.selected_index, len(self.level_files) - 1))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.quit()
                        return None

                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                        self._handle_navigation(event.key)

                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        pygame.display.quit()
                        return self.level_files[self.selected_index]

            self.screen.fill(self.BG_COLOR)
            self._draw_header()
            self._draw_grid()

            pygame.display.flip()
            self.clock.tick(30)
