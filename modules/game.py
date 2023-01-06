import pygame
from .engine import *
from .level import Level
from .player import Player
from .npc import load_npc_sprites

class Game:

    GRASSY = 0
    ROCKY = 1
    CORRIDOR = 2

    def __init__(self, master):

        self.master = master
        self.master.game = self
        self.screen = pygame.display.get_surface()

        self.master.offset = pygame.Vector2(0, 0)

        self.player = Player(master)
        load_npc_sprites()
        self.npc_grp = CustomGroup()
        self.rock_level = Level(master, "rocky_test")
        self.grass_level = Level(master, "grassy_test")
        # self.corridor_level = Level(master, "lol")

        # self.level_index = self.ROCKY
        # self.level = self.rock_level
        self.level = self.grass_level
        self.level.transition_to()

    def run(self):

        self.screen.fill("lightgray")

        self.player.update()
        self.level.update()

        self.level.draw_bg()
        self.player.draw()
        self.level.draw_fg()
