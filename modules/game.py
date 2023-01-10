import pygame
from .engine import *
from .config import *
from .music import Music
from .menus import PauseMenu
from .level import Level, Corridor
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

        self.music = Music(master)
        self.pause_menu = PauseMenu(master)
        load_npc_sprites()  
        load_portal_anims()
        self.player = Player(master)
        # self.rock_level = Level(master, "rocky_test")
        # self.grass_level = Level(master, "grassy_test")

        self.rock_level = Level(master, "rocky_level")
        self.grass_level = Level(master, "grassy_level")
        self.corr = Corridor(master)
        # self.corridor_level = Level(master, "lol")

        self.level_index = self.GRASSY
        # self.level = self.rock_level
        self.level = self.grass_level
        self.level.transition_to()

        self.transitioning = None

        self.black_surf = pygame.Surface(self.screen.get_size())
        self.fade_alpha = 0
        self.fading = 0

        self.paused = False

        self.end_start = False

        self.ending = -1
        self.CORRIDOR = False
        self.to_corridor = False
        self.end_screen = False
        self.vingette = pygame.image.load("graphics/other/vingette.png").convert_alpha()

        self.TRANSITION_CORRIDOR = CustomTimer()
        self.TRANSITION_CORRIDOR2 = CustomTimer()
        self.TRANSITION_CORRIDOR3 = CustomTimer()

        self.THANKS = CustomTimer()

        self.title_surf = self.master.font_big.render('Thanks For Playing', False, (163, 32, 28))
        self.title_rect = self.title_surf.get_rect(center=(W/2, H/2))
        self.title_shadow = self.master.font_big.render('Thanks For Playing', False, (105, 75, 105))
        self.title_shadow.set_alpha(200)

    def pause_game(self):

        if not self.paused:
            self.paused = True
            self.pause_menu.open()

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
            if self.to_corridor:
                self.CORRIDOR = True
                self.level = self.corr
                self.corr.transition_to()
                self.player.dying = False
                self.player.transition_state = "sitting"
                self.player.anim_index = 0
                return
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

    def run_end_check(self):

        if self.TRANSITION_CORRIDOR.check():
            if self.level.dg_manager.active:
                self.level.dg_manager.active.interacting = False
            self.level.dg_manager.active = None
            self.level.dg_manager.interacting = False
            self.end_start = True
            self.player.in_control = False
            self.TRANSITION_CORRIDOR2.start(3_000)
        
        if self.TRANSITION_CORRIDOR2.check():
            self.player.dying = True
            self.player.anim_index = 0
            self.TRANSITION_CORRIDOR3.start(3_000)

        if self.TRANSITION_CORRIDOR3.check():
            self.transitioning = True
            self.fade_alpha = 0
            self.fading = 1
            self.to_corridor = True

        if self.THANKS.check():
            self.end_screen = True

    def run(self):

        self.music.run()

        if self.paused:
            self.pause_menu.draw()
            self.pause_menu.update()
            return

        self.player.update()
        self.level.update()
        if self.transitioning is not None:
            self.update_transition()

        self.run_end_check()

        self.level.draw_bg()
        self.player.draw()
        self.level.draw_fg()

        if self.end_start and not self.CORRIDOR:
            self.screen.blit(self.vingette, (0, 0))

        if self.transitioning is not None:
            self.black_surf.set_alpha(int(self.fade_alpha))
            self.screen.blit(self.black_surf, (0, 0))

        if self.end_screen:
            self.screen.fill(0xb5737c)
            self.screen.blit(self.title_shadow, (self.title_rect.x-2, self.title_rect.y+2))
            self.screen.blit(self.title_surf, self.title_rect)
