import pygame
import os
import math
from .engine import *
from .config import *

DIALOGUES = {}

for file in os.listdir("data/dialogues"):

    DIALOGUES[file[:-4]] = []
    page = []
    with open("data/dialogues/"+file) as f:
        for line in f.read().splitlines():
            line = line.strip()

            if line == "<p>" or line == "<e>":
                DIALOGUES[file[:-4]].append("\n".join(page))
                page = []
            elif line:
                page.append(line)

# for file in os.listdir("data/dialogues"):

#     name = file[:-4]
#     DIALOGUES[name] = {False:[], True:[]}

#     with open("data/dialogues/"+file) as f:
#         initial = True
#         page = []
#         for line in f.read().splitlines():
#             line = line.strip()

#             if line == "<p>":
#                 DIALOGUES[name][not initial].append("\n".join(page))
#                 page = []
#             elif line == "<e>":
#                 DIALOGUES[name][not initial].append("\n".join(page))
#                 if initial: initial = False
#                 page = []
#             elif line:
#                 page.append(line)

# import json
# print(json.dumps(DIALOGUES, indent=2))

class DialogueInteract(pygame.sprite.Sprite):

    def __init__(self, master, grps, rect, type):

        super().__init__(grps)
        self.master = master
        self.rect = pygame.Rect(rect)
        self.type = type
        self.interacted = False

class DialogueManager:

    def __init__(self, master):

        self.master = master
        self.screen = pygame.display.get_surface()

        self.dialogue_grp = CustomGroup()
        self.active:DialogueInteract = None

        self.interact_button_surf = pygame.image.load("graphics/ui/interact_button.png").convert_alpha()
        self.dialogue_box_surf = pygame.image.load("graphics/ui/dialogue_box.png").convert_alpha()
        self.button_rect = self.interact_button_surf.get_rect()

        self.interacting = False
        self.page_index = 0
        self.text_pos = W//2 - 150+12, H-64-8+12-3
    
    def add(self, rect, type):

        DialogueInteract(self.master, [self.dialogue_grp], rect, type)

    def check_near(self):
        
        near = []
        for dg in self.dialogue_grp.sprites():
            if dg.rect.collidepoint(self.master.player.hitbox.center):
                near.append(dg)

        if near:
            self.active = min(near, key = lambda dg: dist_sq(self.master.player.hitbox.center, dg.rect.center))
        else: self.active = None

    def check_interact(self):

        if self.active is None or self.interacting: return

        self.master.player.in_control = False
        self.interacting = True
        self.master.player.facing_right = self.active.rect.centerx > self.master.player.hitbox.centerx
        self.page_index = 0

    def draw(self):

        for dg in self.dialogue_grp.sprites():
            pos = dg.rect.topleft+self.master.offset
            pygame.draw.rect(self.screen, "blue", (*pos, dg.rect.width, dg.rect.height), 1)

        if self.active and not self.interacting:
            self.button_rect.midbottom = self.active.rect.midtop
            self.button_rect.y += math.sin(pygame.time.get_ticks()/200) * 6
            self.screen.blit(self.interact_button_surf, self.button_rect.topleft+self.master.offset)
        elif self.interacting:
            self.draw_dialogue()

    def draw_dialogue(self):

        self.screen.blit(self.dialogue_box_surf, (W//2 - 150, H-64-8))

        try:
            for i, line in enumerate(DIALOGUES[self.active.type][self.page_index].splitlines()):
                pos = self.text_pos[0], self.master.font_1.size("")[1]*i + self.text_pos[1]
                text = self.master.font_1.render(line, False, 0x0)
                self.screen.blit(text, pos)
        except IndexError:
            self.interacting = False
            self.master.player.in_control = True

    def run_dialogue_box(self):
        
        for event in pygame.event.get((pygame.KEYDOWN)):

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.page_index += 1

    def update(self):

        if self.interacting:
            self.run_dialogue_box()
        else:
            self.check_near()
        

