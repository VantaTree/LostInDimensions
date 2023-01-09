import pygame
import csv
from math import ceil
from .config import *
from .engine import *
from .npc import NPC
from .dialogue import DialogueManager
from .portal import Portal

MAP_CONFIG = {  
    "rocky_level":{
        "size": (120, 68),
        "start_pos": (903, 143),
        "portal-0": ((32, 1040), "red"),
        "portal-1": ((1872, 175), "yellow"),
        "parallax_surf": ["back", "middle", "near"],
        "parallax_off":[(W/2, 160), (W/2, 160), (W/2, 160)], #640
        "parallax_v":[(.2, 1), (.3, 1), (.4, 1)],
    },   
    "grassy_level":{
        "size": (120, 68),
        "start_pos": (888, 559),
        "portal-0": ((52, 143), "yellow"),
        "portal-1": ((1885, 735), "red"),
        "parallax_surf": ["back_g", "middle_g"],
        "parallax_off":[(W/2, 128), (W/2, 128)], #608
        "parallax_v":[(.3, 1), (.4, 1)],
    }   
}

NPC_CONFIG = {
    "rocky_level":[
        {"pos": (115, 23), "type":"dino"},
        {"pos": (60, 10), "type":"dog"},
        {"pos": (7, 40), "type":"patient", "anim_speed":0.1},
        {"pos": (48, 59), "type":"skeleton"},
        {"pos": (113, 52), "type":"slimer"},
        {"pos": (88, 65), "type":"tooth_walker"},
        {"pos": (26, 25), "type":"vulture"},
    ],
    "grassy_level":[
        {"pos": (32, 4), "type":"doctor", "anim_speed":0.1},
        {"pos": (6, 46), "type":"necro"},
        {"pos": (97, 4), "type":"eye_ball"},
        {"pos": (41, 50), "type":"nurse", "anim_speed":0.1},
        {"pos": (114, 15), "type":"piranha"},
        {"pos": (62, 16), "type":"witch"},
    ]
}

DIALOGUE_CONFIG = {
    "rocky_level":[
        {"rect":(675, 128, 45, 48), "type":"green_tree"},
        {"rect":(16, 768, 8, 32), "type":"nothing"},
        {"rect":(16, 608, 8, 32), "type":"nothing"},
        {"rect":(1408, 1008, 48, 48), "type":"many_crystals"},
    ],
    "grassy_level":[
        {"rect":(940, 124, 64, 36), "type":"a_house"},
        {"rect":(1896, 1008, 8, 32), "type":"nothing"},
        {"rect":(1896, 224, 8, 32), "type":"nothing"},
        {"rect":(16, 400, 8, 32), "type":"nothing"},
        {"rect":(896, 512, 48, 48), "type":"beautiful_tree"},
        {"rect":(672, 720, 16, 32), "type":"stick"},
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

        self.load_parallax()

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

    def load_parallax(self):

        self.p_imgs = []
        for surf in MAP_CONFIG[self.map_type]["parallax_surf"]:
            img = pygame.image.load(F"graphics/maps/parallax/{surf}.png")
            img = pygame.transform.scale2x(img)
            self.p_imgs.append(img)

        self.p_offsets = MAP_CONFIG[self.map_type]["parallax_off"]
        self.p_vec = MAP_CONFIG[self.map_type]["parallax_v"]

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

        if self.master.offset.y > 0: self.master.offset.y = 0
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

        if self.map_type == "grassy_level":
            self.screen.fill(0x747029)
        elif self.map_type == "rocky_level":
            self.screen.fill(0xc06872)

        for offset, vec, img in zip(self.p_offsets, self.p_vec, self.p_imgs):
            pos = self.master.offset.x *vec[0] +offset[0], \
                self.master.offset.y *vec[1] +offset[1]
            for i in range(ceil(pos[0]/img.get_width())):
                self.screen.blit(img, (pos[0]+ (i+1)*img.get_width()*-1, pos[1]))
            for i in range(ceil((W-pos[0])/img.get_width())):
                self.screen.blit(img, (pos[0]+ i*img.get_width(), pos[1]))



        self.screen.blit(self.map_surf, self.master.offset)
        
        # for y, row in enumerate(self.collision):
        #     for x, cell in enumerate(row):
        #         if cell == 1:
        #             pygame.draw.polygon(self.screen, 'green', ( ((x*TILESIZE, y*TILESIZE+TILESIZE)+self.master.offset).xy,
        #             ((x*TILESIZE+TILESIZE, y*TILESIZE+TILESIZE)+self.master.offset).xy, ((x*TILESIZE+TILESIZE, y*TILESIZE)+self.master.offset).xy ), 1)
        #         elif cell == 2:
        #             pygame.draw.polygon(self.screen, 'green', ( ((x*TILESIZE, y*TILESIZE+TILESIZE)+self.master.offset).xy,
        #             ((x*TILESIZE+TILESIZE, y*TILESIZE+TILESIZE)+self.master.offset).xy, ((x*TILESIZE, y*TILESIZE)+self.master.offset).xy ), 1)
        #         elif cell == 3:
        #             pygame.draw.rect(self.screen, "green", (x*TILESIZE+self.master.offset.x, y*TILESIZE+self.master.offset.y, TILESIZE, TILESIZE), 1)
        #         elif cell == 4:
        #             pygame.draw.rect(self.screen, "green", (x*TILESIZE+self.master.offset.x, y*TILESIZE+self.master.offset.y, TILESIZE, TILESIZE//4), 1)

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
