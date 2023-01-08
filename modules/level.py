import pygame
import csv
from .config import *
from .engine import *
from .npc import NPC
from .dialogue import DialogueManager
from .portal import Portal

MAP_CONFIG = {
    "rocky_test":{
        "size": (48, 16),
        "start_pos" : (32, 207),
        "portal-0": ((32, 207), "red"),
        "portal-1": ((455, 111), "yellow"),
    },
    "grassy_test":{
        "size": (48, 32),
        "start_pos": (40, 397),
        "portal-0": ((40, 397), "yellow"),
        "portal-1": ((536, 495), "red"),
    }   
}

NPC_CONFIG = {
    "rocky_test":[
        {"pos": (28, 6), "type":"slimer"},
    ],
    "grassy_test":[
        {"pos": (31, 12), "type":"witch"},
        {"pos": (27, 15), "type":"dino"},
        {"pos": (39, 20), "type":"doctor", "anim_speed":0.1},
        {"pos": (37, 24), "type":"dog"},
        {"pos": (19, 19), "type":"eye_ball"},
        {"pos": (43, 18), "type":"necro"},
        {"pos": (32, 30), "type":"nurse", "anim_speed":0.1},
        {"pos": (30, 30), "type":"patient", "anim_speed":0.1},
        {"pos": (20, 30), "type":"piranha"},
        {"pos": (23, 30), "type":"skeleton"},
        {"pos": (26, 19), "type":"slimer"},
        {"pos": (18, 30), "type":"tooth_walker"},
        {"pos": (15, 11), "type":"vulture"},
    ]
}

DIALOGUE_CONFIG = {
    "rocky_test":[
        {"rect":(16, 165, 64, 64), "type":"green_tree"},
    ],
    "grassy_test":[
        {"rect":(64, 350, 64, 64), "type":"a_house"},
    ]
}

class Level:

    def __init__(self, master, map_type):
        
        self.master = master
        self.screen = pygame.display.get_surface()
        
        self.map_type = map_type
        self.size = MAP_CONFIG[map_type]["size"]

        self.map_surf = pygame.image.load(F"graphics/maps/{map_type}.png")
        self.collision = self.load_csv(F"data/maps/{map_type}/_collision.csv", True)

        self.dg_manager = DialogueManager(master)
        self.load_dialogues()

        self.npc_grp = CustomGroup()
        self.load_npcs()

        self.portal0 = Portal(master, self, *MAP_CONFIG[self.map_type]["portal-0"], 0)
        self.portal1 = Portal(master, self, *MAP_CONFIG[self.map_type]["portal-1"], 1)

    @staticmethod
    def load_csv(path, integer=False):

        reader = csv.reader(open(path))
        if integer:
            grid = []
            for row in reader:
                grid.append( [int(cell) for cell in row] )
        else:
            grid = [row for row in reader]

        return grid

    def load_dialogues(self):

        for dg in DIALOGUE_CONFIG[self.map_type]:

            self.dg_manager.add(**dg)

    def load_npcs(self):

        for npc in NPC_CONFIG[self.map_type]:
            NPC(self.master, [self.npc_grp], self, **npc)

    def snap_offset(self):

        self.master.offset =  (self.master.player.hitbox.center - pygame.Vector2(W/2, H/2)) * -1

    def update_offset(self):

        camera_rigidness = 0.18 if self.master.player.moving else 0.05
        self.master.offset -= (self.master.offset + (self.master.player.hitbox.center - pygame.Vector2(W/2, H/2)))\
            * camera_rigidness * self.master.dt

    def clamp_offset(self):

        if self.master.offset.x > 0: self.master.offset.x = 0
        elif self.master.offset.x < -self.size[0]*TILESIZE + W:
            self.master.offset.x = -self.size[0]*TILESIZE + W

        # if self.master.offset.y > 0: self.master.offset.y = 0
        if self.master.offset.y < -self.size[1]*TILESIZE + H:
            self.master.offset.y = -self.size[1]*TILESIZE + H

    def transition_to(self, portal_index=None):

        if portal_index is None:
            pos = MAP_CONFIG[self.map_type]["start_pos"]
        else:
            pos = MAP_CONFIG[self.map_type][F"portal-{portal_index}"][0]

        self.master.player.hitbox.midbottom = pos

        self.snap_offset()
        self.clamp_offset()

    def draw_bg(self):

        self.screen.blit(self.map_surf, self.master.offset)
        
        for y, row in enumerate(self.collision):
            for x, cell in enumerate(row):
                if cell == 1:
                    pygame.draw.polygon(self.screen, 'green', ( ((x*TILESIZE, y*TILESIZE+TILESIZE)+self.master.offset).xy,
                    ((x*TILESIZE+TILESIZE, y*TILESIZE+TILESIZE)+self.master.offset).xy, ((x*TILESIZE+TILESIZE, y*TILESIZE)+self.master.offset).xy ), 1)
                elif cell == 2:
                    pygame.draw.polygon(self.screen, 'green', ( ((x*TILESIZE, y*TILESIZE+TILESIZE)+self.master.offset).xy,
                    ((x*TILESIZE+TILESIZE, y*TILESIZE+TILESIZE)+self.master.offset).xy, ((x*TILESIZE, y*TILESIZE)+self.master.offset).xy ), 1)
                elif cell == 3:
                    pygame.draw.rect(self.screen, "green", (x*TILESIZE+self.master.offset.x, y*TILESIZE+self.master.offset.y, TILESIZE, TILESIZE), 1)
                elif cell == 4:
                    pygame.draw.rect(self.screen, "green", (x*TILESIZE+self.master.offset.x, y*TILESIZE+self.master.offset.y, TILESIZE, TILESIZE//4), 1)

        self.portal0.draw()
        self.portal1.draw()
        self.npc_grp.draw()

    def draw_fg(self):

        if self.master.player.in_control or self.dg_manager.interacting: self.dg_manager.draw()

    def update(self):

        self.update_offset()
        self.clamp_offset()
        self.dg_manager.update()
        self.npc_grp.update()
        self.portal0.update()
        self.portal1.update()
