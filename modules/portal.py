import pygame
from .engine import *

PORTAL_ANIMS = {}

def load_portal_anims():

    PORTAL_ANIMS.update(import_sprite_sheets("graphics/portals"))

class Portal:

    def __init__(self, master, level, pos, color, index):

        self.master = master
        self.screen = pygame.display.get_surface()
        self.level = level

        self.color = color
        self.pos = pos
        self.index = index

        self.animation = PORTAL_ANIMS[color]
        self.image:pygame.Surface = self.animation[0]
        self.rect:pygame.Rect = self.image.get_rect(midbottom=pos)
        self.anim_index = 0
        self.anim_speed = 0.15

        level.dg_manager.add(self.rect, "portal")

    def update_image(self):

        try: 
            self.image = self.animation[int(self.anim_index)]
        except IndexError:
            self.anim_index = 0
            self.image = self.animation[0]

        self.anim_index += self.anim_speed *self.master.dt

    def draw(self):

        self.screen.blit(self.image, self.rect.topleft+self.master.offset)

    def update(self):

        self.update_image()