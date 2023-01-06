import pygame
from .engine import *

NPC_ANIMS = {}

def load_npc_sprites():
    NPC_ANIMS.update(import_sprite_sheets("graphics/npcs"))

class NPC(pygame.sprite.Sprite):

    def __init__(self, master, grps, pos, type, anim_speed=0.15, flip=False):

        super().__init__(grps)

        self.master = master
        self.screen = pygame.display.get_surface()

        self.type = type
        self.pos = pos

        self.animation = NPC_ANIMS[type]
        self.image:pygame.Surface = self.animation[0]
        self.rect = self.image.get_rect(midbottom=pos)

        self.anim_index = 0
        self.anim_speed = anim_speed
        self.flip = flip

    def update_image(self):

        try:
            image = self.animation[int(self.anim_index)]
        except IndexError:
            image = self.animation[0]
            self.anim_index = 0

        self.anim_index += self.anim_speed *self.master.dt

        self.image = pygame.transform.flip(image, self.flip, False)

    def draw(self):

        self.screen.blit(self.image, self.rect.topleft+self.master.offset)

    def update(self):

        self.update_image()
