import pygame
from .engine import *
from .level import Level
from .player import Player
from .npc import load_npc_sprites
from .portal import load_portal_anims

class Game:

    GRASSY = 0
    ROCKY = 1
    CORRIDOR = 2

    def __init__(self, master):

        self.master = master
        self.master.game = self
        self.screen = pygame.display.get_surface()

        self.master.offset = pygame.Vector2(0, 0)

        load_npc_sprites()
        load_portal_anims()
        self.player = Player(master)
        self.rock_level = Level(master, "rocky_test")
        self.grass_level = Level(master, "grassy_test")
        # self.corridor_level = Level(master, "lol")

        self.level_index = self.GRASSY
        # self.level = self.rock_level
        self.level = self.grass_level
        self.level.transition_to()

        self.transitioning = None

        self.black_surf = pygame.Surface(self.screen.get_size())
        self.fade_alpha = 0
        self.fading = 0

    def entered_portal(self):

        if self.level.portal0.rect.collidepoint(self.player.hitbox.center):
            self.transitioning = 1
        elif self.level.portal1.rect.collidepoint(self.player.hitbox.center):
            self.transitioning = 0

        self.player.in_control = False
        self.player.transition_state = "to_sit"

    def update_transition(self):

        if self.player.transition_state == "sitting" and not self.fading:
            self.fade_alpha = 0
            self.fading = 1

        self.fade_alpha += self.fading*2 *self.master.dt

        if self.fade_alpha > 255:
            self.fading = -1
            if self.level_index == self.ROCKY:
                self.level_index = self.GRASSY
                self.level = self.grass_level
            else:
                self.level_index = self.ROCKY
                self.level = self.rock_level

            self.level.transition_to(self.transitioning)
        if self.fade_alpha < 0:
            self.transitioning = None
            self.fading = 0
            self.fade_alpha = 0

    def run(self):

        self.screen.fill("lightgray")

        self.player.update()
        self.level.update()
        if self.transitioning is not None:
            self.update_transition()

        self.level.draw_bg()
        self.player.draw()
        self.level.draw_fg()

        if self.transitioning is not None:
            self.black_surf.set_alpha(int(self.fade_alpha))
            self.screen.blit(self.black_surf, (0, 0))
