import pygame
from .config import *
from .engine import *

NPC_ANIMS = {}

def load_npc_sprites():
    NPC_ANIMS.update(import_sprite_sheets("graphics/npcs"))

class NPC(pygame.sprite.Sprite):

    def __init__(self, master, grps, level, pos, type, anim_speed=0.15, flip=False):

        super().__init__(grps)

        self.master = master
        self.screen = pygame.display.get_surface()

        self.type = type
        self.pos = pos[0]*TILESIZE + TILESIZE//2, pos[1]*TILESIZE+TILESIZE-1

        self.animation = NPC_ANIMS[type]
        self.image:pygame.Surface = self.animation[0]
        self.rect = self.image.get_rect(midbottom=self.pos)

        self.anim_index = 0
        self.anim_speed = anim_speed
        self.flip = flip

        self.state = "init"

        self.SIGNAL = CustomTimer()

        self.dialogue = level.dg_manager.add(self.rect.inflate(32, 0), type+"_init", is_npc=self)

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

        check_dialogue[self.type](self)
        self.update_image()


def dino(self:NPC):

    if self.SIGNAL.check():

        if self.state == "init":
            self.state = "bandage"
        elif self.dialogue.type == "dino_bandage" and self.state == "bandage":
            self.master.player.inventory.remove(self.state)
            self.state = "happy"

    if self.state == "bandage" and self.state in self.master.player.inventory:
        self.dialogue.type = "dino_bandage"
        self.dialogue.interacted = False

def doctor(self:NPC):
    
    if self.SIGNAL.check():

        if self.state == "init":
            self.state = "nothing"
            self.master.player.inventory.add("unlit torch")

def dog(self:NPC):
    
    if self.SIGNAL.check():
        if self.state == "init":
            self.state = "play"

        elif self.dialogue.type == "dog_play" and self.state == "play":
            self.master.player.inventory.remove("stick")
            self.master.player.inventory.add("insect")
            self.state = "happy"

    if self.state == "play" and "stick" in self.master.player.inventory:
        self.dialogue.type = "dog_play"
        self.dialogue.interacted = False

def eye_ball(self:NPC):
    
    if self.SIGNAL.check():
        if self.state == "init":
            self.state = "nothing"
            self.master.player.inventory.add("melody box")

def necro(self:NPC):
    
    if self.SIGNAL.check():
        if self.state == "init":
            self.state = "search"

        elif self.dialogue.type == "necro_torch_bone" and self.state == "search":
            self.master.player.inventory.remove("bone hand")
            self.master.player.inventory.remove("unlit torch")
            self.master.player.inventory.add("burning torch")
            self.state = "nothing"

    if self.state == "search":
        if "unlit torch" in self.master.player.inventory and "bone hand" in self.master.player.inventory:
            self.dialogue.type = "necro_torch_bone"
            self.dialogue.interacted = False
        elif "unlit torch" in self.master.player.inventory:
            self.dialogue.type = "necro_torch"
            self.dialogue.interacted = False
        elif "bone hand" in self.master.player.inventory:
            self.dialogue.type = "necro_bone"
            self.dialogue.interacted = False
    
def nurse(self:NPC):
    
    if self.SIGNAL.check():
        if self.state == "init":
            self.state = "scared"

        elif self.dialogue.type == "nurse_calm" and self.state == "scared":
            self.master.player.inventory.remove("melody box")
            self.master.player.inventory.add("knife hand")
            self.state = "calm"

    if self.state == "scared" and "melody box" in self.master.player.inventory:
        self.dialogue.type = "nurse_calm"
        self.dialogue.interacted = False

def patient(self:NPC):
    
    if self.SIGNAL.check():
        if self.state == "init":
            self.state = "med"

        elif self.dialogue.type == "patient_med" and self.state == "med":
            self.master.player.inventory.remove("medicine")
            self.master.player.inventory.add("bandage")
            self.state = "heal"

    if self.state == "med" and "medicine" in self.master.player.inventory:
        self.dialogue.type = "patient_med"
        self.dialogue.interacted = False

def piranha(self:NPC):
    
    if self.SIGNAL.check():
        if self.state == "init":
            self.state = "hungry"

        elif self.dialogue.type == "piranha_fed" and self.state == "hungry":
            self.master.player.inventory.remove("insect")
            self.master.player.inventory.add("herb")
            self.state = "fed"

    if self.state == "hungry" and "insect" in self.master.player.inventory:
        self.dialogue.type = "piranha_fed"
        self.dialogue.interacted = False

def skeleton(self:NPC):
    
    if self.SIGNAL.check():
        if self.state == "init":
            self.state = "cool"

        elif self.dialogue.type == "skeleton_knife" and self.state == "cool":
            self.master.player.inventory.remove("knife hand")
            self.master.player.inventory.add("bone hand")
            self.state = "dance"

    if self.state == "cool" and "knife hand" in self.master.player.inventory:
        self.dialogue.type = "skeleton_knife"
        self.dialogue.interacted = False

def slimer(self:NPC):
    
    if self.SIGNAL.check():
        if self.state == "init":
            self.state = "sad"

        elif self.dialogue.type == "slimer_wife" and self.state == "sad":
            self.master.player.inventory.remove("feather")
            self.state = "happy"

    if self.state == "sad" and "feather" in self.master.player.inventory:
        self.dialogue.type = "slimer_wife"
        self.dialogue.interacted = False

def tooth_walker(self:NPC):
    
    if self.SIGNAL.check():
        if self.state == "init":
            self.state = "hungry"

        elif self.dialogue.type == "tooth_walker_fed" and self.state == "hungry":
            self.master.player.inventory.remove("burning torch")
            self.master.player.inventory.add("shiny crystal")
            self.state = "fed"

    if self.state == "hungry" and "burning torch" in self.master.player.inventory:
        self.dialogue.type = "tooth_walker_fed"
        self.dialogue.interacted = False

def vulture(self:NPC):
    
    if self.SIGNAL.check():
        if self.state == "init":
            self.state = "stare"

        elif self.dialogue.type == "vulture_shiny" and self.state == "stare":
            self.master.player.inventory.remove("shiny crystal")
            self.master.player.inventory.add("feather")
            self.state = "shiny"

    if self.state == "stare" and "shiny crystal" in self.master.player.inventory:
        self.dialogue.type = "vulture_shiny"
        self.dialogue.interacted = False

def witch(self:NPC):
    
    if self.SIGNAL.check():
        if self.state == "init":
            self.state = "wait"

        elif self.dialogue.type == "witch_potion" and self.state == "wait":
            self.master.player.inventory.remove("herb")
            self.master.player.inventory.add("medicine")
            self.state = "potion"

    if self.state == "wait" and "herb" in self.master.player.inventory:
        self.dialogue.type = "witch_potion"
        self.dialogue.interacted = False


check_dialogue = {"dino":dino, "doctor":doctor, "dog":dog, "eye_ball": eye_ball, "necro":necro,
    "nurse":nurse, "patient":patient, "piranha":piranha, "skeleton":skeleton, "slimer":slimer,
    "tooth_walker":tooth_walker, "vulture":vulture, "witch":witch}

