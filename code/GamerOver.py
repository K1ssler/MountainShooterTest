import sys

import pygame
from pygame import Surface, Rect
from pygame.font import Font
from code.Const import C_GREEN, WIN_WIDTH, WIN_HEIGHT, C_ORANGE, C_RED, C_WHITE, GOVER_OPTION


class GameOver:
    def __init__(self, window: Surface):
        self.window = window
        self.surf = pygame.image.load('./asset/GameOver.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)
        self.options = GOVER_OPTION
        self.option_names = list(self.options.keys())
        self.selected_index = 0
        self.sound = pygame.mixer.Sound('./asset/GameOver.wav')

    def show(self):
        self.window.blit(self.surf, self.rect)
        self.Game_Over_text(80, "Game Over", C_RED, (142, 50))

        for i, name in enumerate(self.option_names):
            pos = self.options[name]
            color = C_ORANGE if i == self.selected_index else C_WHITE
            self.Game_Over_text(30, name, color, pos)

    def Game_Over_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(text_surf, text_rect)

    def update_selection(self, direction: str) -> str:
        if direction == "left":
            self.selected_index = (self.selected_index - 1) % len(self.option_names)
        elif direction == "right":
            self.selected_index = (self.selected_index + 1) % len(self.option_names)
        return self.option_names[self.selected_index]

    def run(self) -> str:
        self.sound.play()

        clock = pygame.time.Clock()
        while True:
            self.window.fill((0, 0, 0))
            self.show()
            pygame.display.flip()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_LEFT, pygame.K_a]:
                        self.update_selection("left")
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        self.update_selection("right")
                    elif event.key == pygame.K_RETURN:
                        return self.option_names[self.selected_index]

