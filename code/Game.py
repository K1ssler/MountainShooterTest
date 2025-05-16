#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

import pygame

from code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from code.Level import Level
from code.Menu import Menu
from code.Score import Score
from code.GamerOver import GameOver


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

    def run(self):
        while True:
            score = Score(self.window)
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return == MENU_OPTION[0]:
                player_score = [0]  # [Player1, Player2]
                level = Level(self.window, 'Level1', menu_return, player_score)
                level_return = level.run(player_score)

                if level_return:
                    score.save(menu_return, player_score)
                else:
                    game_over = GameOver(self.window)
                    selected = game_over.run()

                    if selected == "New Game":
                        while True:
                            player_score = [0]
                            level = Level(self.window, 'Level1', menu_return, player_score)
                            level_return = level.run(player_score)
                            if level_return:
                                score.save(menu_return, player_score)
                                break
                            else:
                                game_over = GameOver(self.window)
                                selected = game_over.run()
                                if selected == "Return Menu":
                                    break

                    elif selected == "Return Menu":
                        continue

            elif menu_return == MENU_OPTION[3]:
                score.show()

            elif menu_return == MENU_OPTION[4]:
                pygame.quit()
                quit()

            else:
                pygame.quit()
                sys.exit()

