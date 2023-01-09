import pygame
import os
import math
from .engine import *
from .config import *

DIALOGUES = {}
DIALOGUES_NPC = {}

for file in os.listdir("data/dialogues/simple"):

    DIALOGUES[file[:-4]] = []
    page = []
    with open("data/dialogues/simple/"+file) as f:
        for line in f.read().splitlines():
            line = line.strip()

            if line == "<p>" or line == "<e>":
                DIALOGUES[file[:-4]].append("\n".join(page))
                page = []
            elif line:
                page.append(line)

for file in os.listdir("data/dialogues/npc"):

    name = file[:-4]
    DIALOGUES_NPC[name] = {False:[], True:[]}

    with open("data/dialogues/npc/"+file) as f:
        initial = True
        page = []
        for line in f.read().splitlines():
            line = line.strip()

            if line == "<p>":
                DIALOGUES_NPC[name][not initial].append("\n".join(page))
                page = []
            elif line == "<e>":
                DIALOGUES_NPC[name][not initial].append("\n".join(page))
                if initial: initial = False
                page = []
            elif line:
                page.append(line)

# import json
# print(json.dumps(DIALOGUES_NPC, indent=2))

class DialogueInteract(pygame.sprite.Sprite):

    def __init__(self, master, grps, rect, type, is_npc=None):

        super().__init__(grps)
        self.master = master
        self.rect = rect if isinstance(rect, pygame.Rect) else pygame.Rect(rect)
        self.type = type
        self.interacted = False
        self.is_npc = is_npc
        self.interacting = False

    def send_signal(self):

        if self.type == "stick":
            self.master.player.inventory.add("stick")
            self.kill()

        if not self.is_npc: return
        self.is_npc.SIGNAL.start(0)

class DialogueManager:

    def __init__(self, master):

        self.master = master
        self.screen = pygame.display.get_surface()

        self.dialogue_grp = CustomGroup()
        self.active:DialogueInteract = None

        self.interact_button_surf = pygame.image.load("graphics/ui/interact_button.png").convert_alpha()
        self.dialogue_box_surf = pygame.image.load("graphics/ui/dialogue_box.png").convert_alpha()
        self.button_rect = self.interact_button_surf.get_rect()

        self.icons = load_pngs_dict("graphics/npc_icons")
        self.icons[""] = pygame.Surface((1, 1), pygame.SRCALPHA)

        self.interacting = False
        self.page_index = 0
        self.text_pos = W//2 - 150+12, H-64-8+12-3
    
    def add(self, rect, type, is_npc=False):

        return DialogueInteract(self.master, [self.dialogue_grp], rect, type, is_npc)

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

        self.master.player.facing_right = self.active.rect.centerx > self.master.player.hitbox.centerx
        
        if "portal" in self.active.type:
            self.master.game.entered_portal()
            return

        self.master.player.in_control = False
        self.page_index = 0
        self.interacting = True
        self.active.interacting = True
        if self.active.is_npc:
            self.active.is_npc.flip = self.active.is_npc.rect.centerx > self.master.player.hitbox.centerx

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

        if self.active.is_npc:
            dialogue_page = DIALOGUES_NPC[self.active.type][self.active.interacted]
        else: dialogue_page = DIALOGUES[self.active.type]

        try:
            lines = dialogue_page[self.page_index].splitlines()
            icon = self.icons[lines[0][1:]]
            self.screen.blit(icon, (W//2-150+15-icon.get_width(), H-72+15-icon.get_height()))
        except IndexError:
            self.active.interacted = True
            self.interacting = False
            self.active.interacting = False
            self.master.player.in_control = True
            self.active.send_signal()
            return

        for i, line in enumerate(lines[1:]):
            pos = self.text_pos[0], self.master.font_1.size("")[1]*i + self.text_pos[1]
            text = self.master.font_1.render(line, False, (252, 213, 221))
            self.screen.blit(text, pos)

    def update(self):

        if self.interacting:

            for event in pygame.event.get((pygame.KEYDOWN)):
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.page_index += 1
        else:
            self.check_near()
        

